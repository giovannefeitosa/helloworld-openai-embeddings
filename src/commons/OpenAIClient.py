import os
from commons.Configs import configs
from commons.File import file
import openai
from openai.embeddings_utils import cosine_similarity
import json


class OpenAIClient:
    def __init__(self, debug=False):
        self.debug = debug
        openai.api_key = configs.OPENAI_KEY
        self.embeddingsModel = configs.embeddingsModel

    def generateSyntheticQuestions(self, prompt, debugSentence="", header="", **kwargs):
        # used by prepareutils.Dataset
        """Use OpenAI completion API to generate synthetic questions for each sentence"""
        # ----------------------------------------------
        # generate questions (responseText)
        # ----------------------------------------------
        messages = []
        if header != "":
            messages.append({"role": "user", "content": header})
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=configs.chatCompletionModel,
            messages=messages,
            **kwargs
        )
        responseText = response['choices'][0]['message']['content']
        return response
        # ----------------------------------------------
        # split questions and answers
        # ----------------------------------------------
        # make all question/answers to be on the same line
        # and remove the response header
        try:
            questionAnswers = responseText.replace("\n", "").split('(Q)', 1)[1]
        except IndexError:
            print("Error: responseText: ", debugSentence,
                  '-', response['choices'])
            # TODO: consider doing a retry
            return []
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
        """Generate embeddings for a list of sentences
        returns a list of embeddings (float vectors)
        """
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
            similarity = cosine_similarity(embeddedQuestion, embedding)
            if similarity > maxSimilarity:
                maxSimilarity = similarity
                maxSimilarityIndex = i
        # return the most similar sentence index
        return maxSimilarityIndex


openaiClient = OpenAIClient()
