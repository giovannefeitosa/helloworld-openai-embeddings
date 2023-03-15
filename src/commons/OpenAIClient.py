import os
from commons.Configs import configs
from commons.File import file
import openai
from openai.embeddings_utils import cosine_similarity
import json


class OpenAIClient:
    def __init__(self, debug=True):
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

    def generateSyntheticQuestions(self, prompt, debugSentence=""):
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
        # make all question/answers to be on the same line
        # and remove the response header
        questionAnswers = responseText.replace("\n", "").split('(Q)', 1)[1]
        # one line per question/answer
        questionAnswers = questionAnswers.split('(Q)')
        # split question and answers
        questionAnswers = [x.split('(A)', 1) for x in questionAnswers]
        # remove invalid rows and strip
        questionAnswers = [[x[0].strip(), x[1].strip()]
                           for x in questionAnswers if len(x) == 2]
        jsonData = [{"question": x[0], "answer": x[1]}
                    for x in questionAnswers]
        # ----------------------------------------------
        # debug
        if self.debug:
            print("Sentence: ", debugSentence)
            print("Response text: ", responseText)
            print("jsonData: ", json.dumps(jsonData, indent=4))
        # ----------------------------------------------
        return jsonData

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

    def searchBestEmbeddingIndex(self, embeddedQuestion, embeddingsToSearch):
        # find the most similar sentence
        # used by ask.py
        """Search for the best embedding index"""
        maxSimilarity = 0
        maxSimilarityIndex = 0
        for i, embedding in enumerate(embeddingsToSearch):
            # similarity = cosineSimilarity(
            #     np.array(questionEmbedding['data'][0]['embedding']), embedding)
            similarity = cosine_similarity(embeddedQuestion, embedding)
            if similarity > maxSimilarity:
                maxSimilarity = similarity
                maxSimilarityIndex = i
        # return the most similar sentence index
        return maxSimilarityIndex
        # return the most similar embedding
        # return df.iloc[maxSimilarityIndex].sentences


openaiClient = OpenAIClient()
