from tqdm import tqdm
from commons.Configs import configs
from commons.File import file
from commons.OpenAIClient import openaiClient
from commons.SpacyUtils import spacyUtils


class Dataset:
    def __init__(self, debug=False):
        self.debug = debug

    # Receives an <inputFile>
    # generate synthetic questions and answers
    # save to io/generated/dataset.json
    def generateDatasetFromFile(self, inputFile):
        outputFile = configs.generatedDatasetPath
        # allQaRows is an array where each item is a dict with {"question","answer"} keys
        # ? should I use a list of tuples instead?
        allQaRows = []
        print("Reading input file: ", inputFile)
        text = file.readFile(inputFile)
        # split text into sentences and augment each sentence with synthetic questions and answers
        print("Generating questions and answers for each sentence")
        for sent in tqdm(spacyUtils.splitSentences(text)):
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
            genq = openaiClient.generateSyntheticQuestions(
                prompt, debugSentence=sent)
            allQaRows.extend(genq)
            # debug
            if self.debug:
                for x in genq:
                    print("Sentence: ", sent)
                    print("Q: ", x['question'])
                    print("A: ", x['answer'])
        # save all the generated questions and answers in a generated dataset file
        # Default: io/generated/dataset.json
        print("Writing dataset to file: ", outputFile)
        file.writeFile(outputFile, allQaRows)

    def loadDataset(self):
        inputFilePath = configs.generatedDatasetPath
        return file.readJsonFile(inputFilePath)


dataset = Dataset()
