# this is the entrypoint file for the application
# how to make the imports inside $PROJECT_ROOT/src work with venv folder at $PROJECT_ROOT/io/venv
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import os
import openai
import utils
from OpenAIClient import OpenAIClient

openaiClient = OpenAIClient(os.environ['OPENAI_KEY'])

sampleFilePath = os.path.join(
    os.environ['PROJECT_ROOT'], os.environ['SAMPLE_FILE'])

sampleFile = utils.loadFile(sampleFilePath)

sentences = utils.splitSentences(sampleFile)

sampleSentence = sentences[-1]

sampleEmbeddings = openaiClient.embedSentence(sampleSentence)

print(sampleEmbeddings)
