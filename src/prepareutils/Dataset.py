from tqdm import tqdm
from commons.Configs import configs
from commons.File import file
from commons.OpenAIClient import openaiClient
from commons.SpacyUtils import spacyUtils
from commons.PromptUtils import promptUtils
from prompts.FootballPlayerPrompt import FootballPlayerPrompt


class Dataset:
    def __init__(self, debug=True):
        self.debug = debug

    # Receives an <inputFile>Giovanne
    # generate synthetic questions and answers
    # save to io/generated/dataset.json
    def generateDatasetFromFile(self, inputFile):
        outputFile = configs.generatedDatasetPath
        # allQaRows is an array where each item is a dict with {"question","answer"} keys
        # ? should I use a list of tuples instead?
        allQaRows = []
        print("Reading input file: ", inputFile)
        text = file.readFile(inputFile)
        # split text into paragraphs and augment each paragraph with synthetic questions and answers
        print("Generating questions and answers for each paragraph")
        for paragraph in tqdm(spacyUtils.splitParagraphs(text)):
            prompt = FootballPlayerPrompt({"PARAGRAPH": paragraph})
            topics = prompt.retrieveTopics()
            allQaRows.extend(topics)
            # debug
            # if self.debug:
            #    print("Paragraph: ", paragraph)
            #    print("")
            #    for x in topics:
            #        print("Q: ", x['question'])
            #        print("A: ", x['answer'])
            #    exit(0)
        # save all the generated questions and answers in a generated dataset file
        # Default: io/generated/dataset.json
        print("Writing dataset to file: ", outputFile)
        file.writeFile(outputFile, allQaRows)

    def loadDataset(self):
        inputFilePath = configs.generatedDatasetPath
        allQaRows = file.readJsonFile(inputFilePath)
        # -- begin extra dataset
        # insert extra dataset to the beginning of the list
        extraQaRows = file.readJsonFile(
            configs.path('io/data/extraDataset.json'))
        extraQaRows.extend(allQaRows)
        allQaRows = extraQaRows
        # -- end extra dataset
        return allQaRows


dataset = Dataset()
