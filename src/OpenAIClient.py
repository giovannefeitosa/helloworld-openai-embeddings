import openai


class OpenAIClient:
    def __init__(self, key, modelName="text-embedding-ada-002"):
        openai.api_key = key
        self.modelName = modelName

    def embedSentence(self, text):
        text = text.replace("\n", " ")  # question: Do i need this line?
        response = openai.Embedding.create(
            input=[text],
            model=self.modelName,
        )
        return response
