import os


class Configs:
    def __init__(self):
        # environment variables
        self.OPENAI_KEY = os.environ['OPENAI_KEY']
        self.PROMPT_PERSON_NAME = os.environ['PROMPT_PERSON_NAME']
        self.PROMPT_PERSON_SOCIALNAME = os.environ['PROMPT_PERSON_SOCIALNAME']
        self.PROMPT_PERSON_TITLE = os.environ['PROMPT_PERSON_TITLE']
        self.PROMPT_PERSON_HESHEIT = os.environ['PROMPT_PERSON_HESHEIT']
        self.PROMPT_PERSON_BIRTHDAY = os.environ['PROMPT_PERSON_BIRTHDAY']
        self.PROMPT_PERSON_DEATHDAY = os.environ['PROMPT_PERSON_DEATHDAY']
        self.PROMPT_PERSON_BIRTHPLACE = os.environ['PROMPT_PERSON_BIRTHPLACE']
        self.PROMPT_PERSON_DEATHPLACE = os.environ['PROMPT_PERSON_DEATHPLACE']
        self.PROMPT_PERSON_NUMBER_OF_QUESTIONS = os.environ['PROMPT_PERSON_NUMBER_OF_QUESTIONS']
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


configs = Configs()
