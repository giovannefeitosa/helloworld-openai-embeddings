from tqdm import tqdm
import numpy as np
from commons.Configs import configs
from commons.File import file
from commons.OpenAIClient import openaiClient
from prepareutils.Dataset import dataset
import numpy as np
from sklearn import preprocessing


class Embeddings:
    def __init__(self, debug=False):
        self.debug = debug
        self.embeddings = None

    # generate synthetic questions and answers
    # save to io/generated/embeddings.json
    def generateEmbeddings(self):
        print("")
        outputFilePath = configs.generatedEmbeddingsPath
        allQaRows = dataset.loadDataset()
        embeddings = []
        # for each item
        for i, qa in enumerate(tqdm(allQaRows)):
            # make a list of sentences
            sentences = []
            for q in qa['questions']:
                sentences.append(q)
            sentences.append(qa['answer'])
            # generate the embeddings
            emb = openaiClient.generateEmbeddings(sentences)
            embjson = {
                'questions': emb[0:-1],
                'answer': emb[-1],
                'topic': i,
            }
            embeddings.append(embjson)
        # save all the generated embeddings
        # Default: io/generated/embeddings.json
        print("Writing embeddings to file: ", outputFilePath)
        file.writeFile(outputFilePath, embeddings)

    # load embeddings from file
    def loadEmbeddings(self):
        inputFilePath = configs.generatedEmbeddingsPath
        if self.embeddings is None:
            self.embeddings = file.readJsonFile(inputFilePath)
        return self.embeddings
        # questionEmbeddings = [x['question'] for x in embeddings]
        # answerEmbeddings = [x['answer'] for x in embeddings]
        # labels = [x['label'] for x in embeddings]
        # i would use float16, but I've had issues with GPU
        # I know I'm not using GPU now, but I might in the future
        # return \
        #    np.array(questionEmbeddings, dtype=np.float32), \
        #    np.array(answerEmbeddings, dtype=np.float32), \
        #    np.array(labels, dtype=np.int32)

    def getAsXy(self, numberOfAugmentations=6, noiseMin=-0.000003, noiseMax=0.000003):
        embeddings = self.loadEmbeddings()
        questionEmbeddings = []
        labels = []
        topics = []

        for label, emb in enumerate(embeddings):
            npAnswer = np.array(emb['answer'])
            topic = emb['topic']
            for embQuestion in emb['questions']:
                questionEmbeddings.append(np.array(embQuestion) + npAnswer)
                labels.append(label)
                topics.append(topic)

        x, y, tp = \
            np.array(questionEmbeddings, dtype=np.float32), \
            np.array(labels, dtype=np.int32), \
            np.array(topics, dtype=np.int32)

        return self._augmentXy(x, y, tp, numberOfAugmentations, noiseMin, noiseMax)
        # return x, y

    def _augmentXy(self, x, y, tp, numberOfAugmentations, noiseMin, noiseMax):
        """
        Generate new x and y by adding noise to x and y
        """
        newX = x
        newY = y
        print("x, y shapes: ", x.shape, y.shape)
        for oldX, oldY, oldTp in zip(x, y, tp):
            nAugments = numberOfAugmentations
            # the first topic is always unknown
            # before: we won't augment it
            # now: we will augment less than others
            # see: prepareutils.Dataset.Dataset.loadDataset
            if oldTp == 0:
                nAugments = 2

            noises = np.arange(0, nAugments, 1) \
                * np.float32(1 / nAugments) * (noiseMax - noiseMin) + noiseMin
            for noiseK in noises:
                # for i in range(nAugments):
                noisedX = oldX + noiseK
                noisedY = oldY
                # newX = np.append(newX, np.expand_dims(noisedX, axis=0))
                # newY = np.append(newY, np.expand_dims(noisedY, axis=0))
                newX = np.append(newX, np.expand_dims(noisedX, axis=0), axis=0)
                newY = np.append(newY, np.expand_dims(noisedY, axis=0), axis=0)
        print("new x, y shapes: ", newX.shape, newY.shape)
        return newX, newY


embeddings = Embeddings()
