from tqdm import tqdm
import spacy
from commons.Configs import configs
from commons.File import file
from commons.OpenAIClient import openaiClient


class Embeddings:
    def __init__(self, debug=False):
        self.debug = debug

    def generateEmbeddings(self):
        inputFilePath = configs.generatedDatasetPath
        outputFilePath = configs.generatedEmbeddingsPath
        dataset = file.readJsonFile(inputFilePath)
        embeddings = []
        print("")
        # for each sentence
        for qa in tqdm(dataset):
            sentences = [qa['question'], qa['answer']]
            emb = openaiClient.generateEmbeddings(sentences)
            embjson = {'question': emb[0], 'answer': emb[1]}
            embeddings.append(embjson)
        # save all the generated embeddings
        # Default: io/generated/embeddings.json
        print("Writing embeddings to file: ", outputFilePath)
        file.writeFile(outputFilePath, embeddings)


embeddings = Embeddings()
