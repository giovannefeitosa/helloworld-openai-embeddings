# Command:
#   bash manage.sh ask "<question>""
# --------------------------------------------------
import sys
from commons.Model import model
from commons.OpenAIClient import openaiClient
from prepareutils.Dataset import dataset

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
