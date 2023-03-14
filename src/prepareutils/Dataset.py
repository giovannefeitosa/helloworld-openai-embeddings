from tqdm import tqdm
import json
import spacy
import os
from commons.Configs import configs
from commons.File import file
from commons.OpenAIClient import openaiClient


class Dataset:
    def __init__(self, debug=False):
        self.debug = debug

    # Receives an <inputFile>
    # generate synthetic questions and answers
    # save to <outputFile>
    def generateDatasetFromFile(self, inputFile, outputFile):
        # allQaRows is an array where each item is a dict with {"question","answer"} keys
        # ? should I use a list of tuples instead?
        allQaRows = []
        print("Reading input file: ", inputFile)
        text = file.readFile(inputFile)
        # split text into sentences and augment each sentence with synthetic questions and answers
        print("Generating questions and answers for each sentence")
        for sent in tqdm(self.splitSentences(text)):
            prompt = openaiClient.buildPrompt("generateQuestionsPerson", {
                'NAME': configs.PROMPT_PERSON_NAME,
                'SOCIALNAME': configs.PROMPT_PERSON_SOCIALNAME,
                'TITLE': configs.PROMPT_PERSON_TITLE,
                'HESHEIT': configs.PROMPT_PERSON_HESHEIT,
                'BIRTHDAY': configs.PROMPT_PERSON_BIRTHDAY,
                'DEATHDAY': configs.PROMPT_PERSON_DEATHDAY,
                'BIRTHPLACE': configs.PROMPT_PERSON_BIRTHPLACE,
                'DEATHPLACE': configs.PROMPT_PERSON_DEATHPLACE,
                'NUMBER_OF_QUESTIONS': configs.PROMPT_PERSON_NUMBER_OF_QUESTIONS,
                'SENTENCE': sent
            })
            allQaRows.extend(openaiClient.generateSyntheticQuestions(prompt))
            # ----------------------------------------------
            # debug
            if self.debug:
                for x in allQaRows:
                    print("Q: ", x['question'])
                    print("A: ", x['answer'])
            # ----------------------------------------------
        # save all the generated questions and answers in a generated dataset file
        # Default: io/generated/dataset.json
        print("Writing dataset to file: ", outputFile)
        file.writeFile(outputFile, json.dumps(allQaRows))

    # Receives a raw text and returns an array of sentences
    def splitSentences(self, text):
        """Split text into sentences"""
        nlp = self.spacyLoad()
        doc = nlp(text)
        return [sent.text for sent in doc.sents]

    # Returns a spacy.load() model
    def spacyLoad(self):
        """Load spacy model"""
        if not hasattr(self, 'spacyModel'):
            self.spacyModel = spacy.load(configs.spacyModel)
        return self.spacyModel

    # Receives a sentence and returns an array of questions and answers
    # def generatePersonQuestions(self, sentence):
    #    """Use OpenAI completion API to generate synthetic questions for each sentence"""
    #    # TODO: consider reading the prompt file only once
    #    with open(configs.promptFilePath, 'r') as f:
    #        prompt = f.read()
    #    # ----------------------------------------------
    #    # create a fresh prompt
    #    # replacing all variables in our template
    #    # ----------------------------------------------
    #    prompt = prompt.replace("{NAME}", os.environ['PROMPT_PERSON_NAME'])
    #    prompt = prompt.replace(
    #        "{SOCIALNAME}", os.environ['PROMPT_PERSON_SOCIALNAME'])
    #    prompt = prompt.replace("{TITLE}", os.environ['PROMPT_PERSON_TITLE'])
    #    prompt = prompt.replace(
    #        "{HESHEIT}", os.environ['PROMPT_PERSON_HESHEIT'])
    #    prompt = prompt.replace(
    #        "{BIRTHDAY}", os.environ['PROMPT_PERSON_BIRTHDAY'])
    #    prompt = prompt.replace(
    #        "{DEATHDAY}", os.environ['PROMPT_PERSON_DEATHDAY'])
    #    prompt = prompt.replace(
    #        "{BIRTHPLACE}", os.environ['PROMPT_PERSON_BIRTHPLACE'])
    #    prompt = prompt.replace(
    #        "{DEATHPLACE}", os.environ['PROMPT_PERSON_DEATHPLACE'])
    #    prompt = prompt.replace("{NUMBER_OF_QUESTIONS}",
    #                            os.environ['PROMPT_PERSON_NUMBER_OF_QUESTIONS'])
    #    prompt = prompt.replace("{SENTENCE}", sentence)
    #    # ----------------------------------------------
    #    # split questions and answers
    #    # ----------------------------------------------
    #    return self._generateQuestionAnswersFromPrompt(prompt)

    # def _generateQuestionAnswersFromPrompt(self, prompt, debug=False):
    #    """
    #        Use OpenAI completion API to generate synthetic questions for each sentence and
    #        return a list with dicts in the format:
    #        [{"question":"...", "answer":"..."}, {"question":"...", "answer":"..."}]
    #    """
    #    # ----------------------------------------------
    #    # generate questions (responseText)
    #    # ----------------------------------------------
    #    response = openai.ChatCompletion.create(
    #        model=configs.chatCompletionModel,
    #        messages=[{"role": "user", "content": prompt}]
    #    )
    #    responseText = response['choices'][0]['message']['content']
    #    # ----------------------------------------------
    #    # split questions and answers
    #    # ----------------------------------------------
    #    responseText = responseText.replace("(Q) ", "")
    #    questionAnswers = [x.split("(A)") for x in responseText.split("\n")]
    #    questionAnswers = [row for row in questionAnswers if len(row) >= 2]
    #    # ----------------------------------------------
    #    # debug
    #    if debug:
    #        for x in questionAnswers:
    #            print("Q: ", x[0])
    #            print("A: ", x[1])
    #    # ----------------------------------------------
    #    return [{"question": x[0], "answer": x[1]} for x in questionAnswers]


dataset = Dataset()
