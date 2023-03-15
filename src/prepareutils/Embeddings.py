from tqdm import tqdm
import numpy as np
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
        for i, qa in enumerate(tqdm(dataset)):
            sentences = [qa['question'], qa['answer']]
            emb = openaiClient.generateEmbeddings(sentences)
            embjson = {'question': emb[0], 'answer': emb[1], 'label': i}
            print("Sentence: ", i, sentences)
            embeddings.append(embjson)
        # save all the generated embeddings
        # Default: io/generated/embeddings.json
        print("Writing embeddings to file: ", outputFilePath)
        file.writeFile(outputFilePath, embeddings)

    def loadEmbeddings(self):
        inputFilePath = configs.generatedEmbeddingsPath
        embeddings = file.readJsonFile(inputFilePath)
        questionEmbeddings = [x['question'] for x in embeddings]
        answerEmbeddings = [x['answer'] for x in embeddings]
        labels = [x['label'] for x in embeddings]
        # i would use float16, but I've had issues with GPU
        # I know I'm not using GPU now, but I might in the future
        return \
            np.array(questionEmbeddings, dtype=np.float32), \
            np.array(answerEmbeddings, dtype=np.float32), \
            np.array(labels, dtype=np.int32)


embeddings = Embeddings()
