import os
import datetime


class Configs:
    def __init__(self):
        # environment variables
        self.OPENAI_KEY = os.environ['OPENAI_KEY']
        self.promptVariables = {
            'NAME': os.environ['PROMPT_PERSON_NAME'],
            'SOCIALNAME': os.environ['PROMPT_PERSON_SOCIALNAME'],
            'TITLE': os.environ['PROMPT_PERSON_TITLE'],
            'HESHEIT': os.environ['PROMPT_PERSON_HESHEIT'],
            'BIRTHDAY': os.environ['PROMPT_PERSON_BIRTHDAY'],
            'DEATHDAY': os.environ['PROMPT_PERSON_DEATHDAY'],
            'BIRTHPLACE': os.environ['PROMPT_PERSON_BIRTHPLACE'],
            'DEATHPLACE': os.environ['PROMPT_PERSON_DEATHPLACE'],
            'NUMBER_OF_QUESTIONS': os.environ['PROMPT_PERSON_NUMBER_OF_QUESTIONS'],
            'ACHIEVEMENT': os.environ['PROMPT_PERSON_ACHIEVEMENT']
        }
        # openai
        self.chatCompletionModel = "gpt-3.5-turbo"
        self.embeddingsModel = "text-embedding-ada-002"
        # prompt files
        self.promptsDir = f"{os.environ['PROJECT_ROOT']}/io/prompts"
        # generated files
        self.generatedDatasetPath = f"{os.environ['PROJECT_ROOT']}/io/generated/dataset.json"
        self.generatedEmbeddingsPath = f"{os.environ['PROJECT_ROOT']}/io/generated/embeddings.json"
        # spacy
        self.spacyModel = 'en_core_web_sm'
        # model
        self.generatedModelPath = f"{os.environ['PROJECT_ROOT']}/io/generated/model.sklearn"

    def getPromptVariables(self, extraData={}):
        # used by prepareutils.Dataset
        extraData['TODAY'] = datetime.datetime.now().strftime("%Y-%m-%d")
        variables = self.promptVariables
        for key, value in extraData.items():
            variables[key] = value
        return variables

    def path(self, path):
        return f"{os.environ['PROJECT_ROOT']}/{path}"


configs = Configs()
