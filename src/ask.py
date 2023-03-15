# Command:
#   bash manage.sh prepare <txt_file>
# --------------------------------------------------
# This command will create a dataset.json file containing a list of questions and answers
# in json format. This file will be used to generate embeddings.
#
#   io/generated/dataset.json
#
import sys
from commons.Configs import configs
from commons.File import file
from commons.Model import model
from commons.OpenAIClient import openaiClient
from prepareutils.Dataset import dataset
from prepareutils.Embeddings import embeddings
import json

if __name__ == "__main__":
    question = sys.argv[1]
    # load the model
    clf = model.load()
    # embed question
    questionEmbedding = openaiClient.generateEmbeddings([question])[0]
    # predict answer index
    answerIndex = clf.predict([questionEmbedding]).item()
    # load dataset
    qaDataset = dataset.loadDataset()
    # get answer
    bestAnswer = qaDataset[answerIndex]
    # print
    print("Best answer: ")
    print(bestAnswer["answer"])
