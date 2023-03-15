import os
from commons.OpenAIClient import openaiClient
import utils
import numpy as np
import pickle

# sample and embeddings file paths
sampleFilePath = os.path.join(
    os.environ['PROJECT_ROOT'], os.environ['DATA_FILE'])
embeddingsFilePath = os.path.join(
    os.environ['PROJECT_ROOT'], os.environ['EMBEDDINGS_FILE'])


def getSentences():
    # read sample file
    sampleFile = utils.readFile(sampleFilePath)
    # split sentences
    sentences = utils.splitSentences(sampleFile)
    return sentences


# create embeddings
def createEmbeddings(sentences):
    # get sentences' embeddings
    apiEmbeddings = [openaiClient.embedSentence(sent) for sent in sentences]
    # parse embeddings, we just need the vector
    embeddings = [np.array(emb['data'][0]['embedding'])
                  for emb in apiEmbeddings]
    # save embeddings
    with open(embeddingsFilePath, 'wb') as f:
        pickle.dump(embeddings, f)
    return embeddings


# load embeddings
def loadEmbeddings():
    sentences = getSentences()
    # load
    if os.path.exists(embeddingsFilePath):
        print("[loadEmbeddings] Loading embeddings from file...")
        with open(embeddingsFilePath, 'rb') as f:
            embeddings = pickle.load(f)
    # create if not exists
    else:
        print("[loadEmbeddings] Creating embeddings...")
        embeddings = createEmbeddings(sentences)
    # return
    df = pd.DataFrame({'sentences': sentences, 'embeddings': embeddings})
    return df
