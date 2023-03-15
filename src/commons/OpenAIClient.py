import os
from commons.Configs import configs
from commons.File import file
import openai


class OpenAIClient:
    def __init__(self, debug=False):
        self.debug = debug
        openai.api_key = configs.OPENAI_KEY
        self.embeddingsModel = configs.embeddingsModel

    def buildPrompt(self, name, variables):
        # used by prepareutils.Dataset
        promptFilePath = os.path.join(configs.promptsDir, f"{name}.prompt.txt")
        prompt = file.readFile(promptFilePath)
        for key, value in variables.items():
            prompt = prompt.replace(f"{{{key}}}", value)
        return prompt

    def generateSyntheticQuestions(self, prompt):
        # used by prepareutils.Dataset
        """Use OpenAI completion API to generate synthetic questions for each sentence"""
        # ----------------------------------------------
        # generate questions (responseText)
        # ----------------------------------------------
        response = openai.ChatCompletion.create(
            model=configs.chatCompletionModel,
            messages=[{"role": "user", "content": prompt}]
        )
        responseText = response['choices'][0]['message']['content']
        # ----------------------------------------------
        # split questions and answers
        # ----------------------------------------------
        responseText = responseText.replace("(Q) ", "")
        # split by (Q) and (A)
        questionAnswers = [x.split("(A)") for x in responseText.split("\n")]
        # remove invalid rows
        questionAnswers = [row for row in questionAnswers if len(row) >= 2]
        # remove rows with empty sentences
        questionAnswers = [row for row in questionAnswers if row[0].replace(
            ' ', '') != '' and row[1].replace(' ', '') != '']
        # ----------------------------------------------
        # debug
        if self.debug:
            for x in questionAnswers:
                print("Q: ", x[0])
                print("A: ", x[1])
        # ----------------------------------------------
        return [{"question": x[0], "answer": x[1]} for x in questionAnswers]

    def generateEmbeddings(self, sentences):
        # used by prepareutils.Embeddings
        response = openai.Embedding.create(
            input=sentences,
            model=self.embeddingsModel,
        )
        embeddings = []
        for x in response['data']:
            embeddings.append(x['embedding'])
        assert len(embeddings) == len(sentences)
        return embeddings


openaiClient = OpenAIClient()
