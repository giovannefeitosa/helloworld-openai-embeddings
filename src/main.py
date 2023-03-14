# this is the entrypoint file for the application
# how to make the imports inside $PROJECT_ROOT/src work with venv folder at $PROJECT_ROOT/io/venv
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import os
import openai
import utils

openai.api_key = os.environ['OPENAI_KEY']

sampleFilePath = os.path.join(
    os.environ['PROJECT_ROOT'], os.environ['SAMPLE_FILE'])

sampleFile = utils.loadFile(sampleFilePath)

sentences = utils.splitSentences(sampleFile)

print(sentences[-1])
