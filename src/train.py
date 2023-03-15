# Command:
#   bash manage.sh train
# --------------------------------------------------
# This command will train a model to answer questions.
#
#   io/generated/dataset.json
#
import numpy as np
from prepareutils.Embeddings import embeddings
from prepareutils.Dataset import dataset
from commons.OpenAIClient import openaiClient
from commons.Configs import configs
from commons.Model import model


def train():
    print("Training model...")
    # load dataset and embeddings
    qaDataset = dataset.loadDataset()
    questionEmbeddings, answerEmbeddings, labels = embeddings.loadEmbeddings()
    # combine both embeddings and create X, y
    x, y = questionEmbeddings + answerEmbeddings, labels
    clf = model.train(x, y)
    model.save(clf)


if __name__ == "__main__":
    train()
