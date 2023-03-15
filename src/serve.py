import gradio as gr
from commons.Model import model
from commons.OpenAIClient import openaiClient
from prepareutils.Dataset import dataset
import numpy as np

# load the model once
clf = model.load()
# load dataset
qaDataset = dataset.loadDataset()


def predict(question):
    # embed question
    questionEmbedding = openaiClient.generateEmbeddings([question])[0]
    # predict answer index
    answerIndex = clf.predict([questionEmbedding]).item()
    # get answer
    bestAnswer = qaDataset[answerIndex]
    return bestAnswer["answer"]


def randomExamples(numberOfExamples=15):
    # create random indexes in the range between 0 and len(qaDataset)
    randomIndexes = np.random.randint(0, len(qaDataset), numberOfExamples)
    examples = []
    for index in randomIndexes:
        question = qaDataset[index]["question"]
        examples.append([question])
    return examples


gr.Interface(
    fn=predict,
    inputs="text",
    outputs="text",
    examples=randomExamples(),
).launch()
