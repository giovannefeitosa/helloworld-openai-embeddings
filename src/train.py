# Command:
#   bash manage.sh train
# --------------------------------------------------
# This command will train a model to answer questions.
#
#   io/generated/dataset.json
#
from prepareutils.Embeddings import embeddings
from prepareutils.Dataset import dataset
from commons.Model import model


# train the model using sklearn
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
