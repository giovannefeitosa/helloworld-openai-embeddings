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
from commons.OpenAIClient import openaiClient
from prepareutils.Dataset import dataset
from prepareutils.Embeddings import embeddings
import json

if __name__ == "__main__":
    question = sys.argv[1]
    # load dataset and embeddings
    qaDataset = dataset.loadDataset()
    questionEmbeddings, answerEmbeddings = embeddings.loadEmbeddings()
    # search for the best answer
    embeddedQuestion = openaiClient.generateEmbeddings([question])[0]
    bestIndex = openaiClient.searchBestEmbeddingIndex(
        embeddedQuestion,
        questionEmbeddings,
        # questionEmbeddings + answerEmbeddings,
    )
    bestAnswer = qaDataset[bestIndex]
    print("Best answer: ")
    print(f"index: {bestIndex}")
    print(f"answer: {json.dumps(bestAnswer)}")
