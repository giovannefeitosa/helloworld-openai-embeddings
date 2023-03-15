import gradio as gr
from commons.Model import model
from commons.OpenAIClient import openaiClient
from commons.File import file
from commons.Configs import configs
from prepareutils.Dataset import dataset
import numpy as np

# load the model once
clf = model.load()
# load dataset
qaDataset = dataset.loadDataset()


# required files
if not file.exists(configs.generatedEmbeddingsPath):
    print(f"Error: {configs.generatedEmbeddingsPath} does not exist.")
    print("Please run: bash manage.sh prepare <input_file>")
    exit(1)
if not file.exists(configs.generatedDatasetPath):
    print(f"Error: {configs.generatedDatasetPath} does not exist.")
    print("Please run: bash manage.sh prepare <input_file>")
    exit(1)
if not file.exists(configs.generatedModelPath):
    print(f"Error: {configs.generatedModelPath} does not exist.")
    print("Please run: bash manage.sh train")
    exit(1)


# embed the question and predict
def predict(question):
    # embed question
    questionEmbedding = openaiClient.generateEmbeddings([question])[0]
    # predict answer index
    answerIndex = clf.predict([questionEmbedding]).item()
    # get answer
    bestAnswer = qaDataset[answerIndex]
    return bestAnswer["answer"]


# generate random examples
def randomExamples(numberOfExamples=15):
    # create random indexes in the range between 0 and len(qaDataset)
    randomIndexes = np.random.randint(0, len(qaDataset), numberOfExamples)
    examples = []
    for index in randomIndexes:
        question = qaDataset[index]["question"]
        examples.append([question])
    return examples


# launch the gradio interface
gr.Interface(
    fn=predict,
    inputs="text",
    outputs="text",
    examples=randomExamples(),
).launch()
