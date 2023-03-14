# Command:
#   bash manage.sh prepare <txt_file> <output_file>
#
# This command will output two files:
# 1. io/generated/dataset.json
# 2. io/generated/embeddings.json
import sys
import os
import spacy
import json
from commons.OpenAIClient import openaiClient
import openai
from tqdm import tqdm

# OpenAI API key
openai.api_key = os.environ['OPENAI_KEY']
# Prompt file path
promptFilePath = f"{os.environ['PROJECT_ROOT']}/io/prompts/generateQuestionsPerson.prompt.txt"


def prepare(inputFilePath, outputFilePath, debug):
    """
        Command:
            bash manage.sh prepare <txt_file> <output_file>

        Transforms the input file into a dataset file
    """
    # allQaRows is an array where each item is a dict with {"question","answer"} keys
    # ? should I use a list of tuples instead?
    allQaRows = []

    # Read the input text file
    with open(inputFilePath, 'r') as f:
        text = f.read()
    # Split text into sentences and augment each sentence with synthetic questions and answers
    for sent in tqdm(splitSentences(text)):
        allQaRows.extend(generatePersonQuestions(sent, debug=debug))
    # Save the questions and the answers in a generated dataset file
    # Default: io/generated/dataset.json
    with open(outputFilePath, 'w') as f:
        f.write(json.dumps(allQaRows))


# Receives a raw text and returns an array of sentences
def splitSentences(text):
    """Split text into sentences"""
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def generatePersonQuestions(sentence, debug):
    """Use OpenAI completion API to generate synthetic questions for each sentence"""
    # TODO: consider reading the prompt file only once
    with open(promptFilePath, 'r') as f:
        prompt = f.read()
    # ----------------------------------------------
    # create a fresh prompt
    # replacing all variables in our template
    # ----------------------------------------------
    prompt = prompt.replace("{NAME}", os.environ['PROMPT_PERSON_NAME'])
    prompt = prompt.replace(
        "{SOCIALNAME}", os.environ['PROMPT_PERSON_SOCIALNAME'])
    prompt = prompt.replace("{TITLE}", os.environ['PROMPT_PERSON_TITLE'])
    prompt = prompt.replace("{HESHEIT}", os.environ['PROMPT_PERSON_HESHEIT'])
    prompt = prompt.replace(
        "{BIRTHDAY}", os.environ['PROMPT_PERSON_BIRTHDAY'])
    prompt = prompt.replace(
        "{DEATHDAY}", os.environ['PROMPT_PERSON_DEATHDAY'])
    prompt = prompt.replace(
        "{BIRTHPLACE}", os.environ['PROMPT_PERSON_BIRTHPLACE'])
    prompt = prompt.replace(
        "{DEATHPLACE}", os.environ['PROMPT_PERSON_DEATHPLACE'])
    prompt = prompt.replace("{NUMBER_OF_QUESTIONS}",
                            os.environ['PROMPT_PERSON_NUMBER_OF_QUESTIONS'])
    prompt = prompt.replace("{SENTENCE}", sentence)
    # ----------------------------------------------
    # split questions and answers
    # ----------------------------------------------
    return _generateQuestionAnswersFromPrompt(prompt, debug=debug)


def _generateQuestionAnswersFromPrompt(prompt, model="gpt-3.5-turbo", debug=False):
    """
        Use OpenAI completion API to generate synthetic questions for each sentence and
        return a list with dicts in the format:
        [{"question":"...", "answer":"..."}, {"question":"...", "answer":"..."}]
    """
    # ----------------------------------------------
    # generate questions (responseText)
    # ----------------------------------------------
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    responseText = response['choices'][0]['message']['content']
    # ----------------------------------------------
    # split questions and answers
    # ----------------------------------------------
    responseText = responseText.replace("(Q) ", "")
    questionAnswers = [x.split("(A)") for x in responseText.split("\n")]
    questionAnswers = [row for row in questionAnswers if len(row) >= 2]
    # ----------------------------------------------
    # debug
    if debug:
        for x in questionAnswers:
            print("Q: ", x[0])
            print("A: ", x[1])
    # ----------------------------------------------
    return [{"question": x[0], "answer": x[1]} for x in questionAnswers]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: missing arguments")
        print("Usage: bash manage.py prepare <input_file_path>\n")
        sys.exit(1)
    # read arguments
    inputFilePath = sys.argv[1]
    outputFilePath = "io/generated/dataset.json"
    # process
    prepare(inputFilePath, outputFilePath, debug=False)
