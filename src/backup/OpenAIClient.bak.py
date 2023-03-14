import os
import openai
from openai.embeddings_utils import cosine_similarity
from numpy import dot
from numpy.linalg import norm
import numpy as np


# https://stackoverflow.com/a/43043160/1791115
def cosineSimilarity(embedding1, embedding2):
    return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))


promptGenerateQuestion = """
    Question: test
    hi : tests
""".strip()


class OpenAIClient:
    def __init__(self, key, embeddingModel="text-embedding-ada-002", completionModel="gpt-3.5-turbo"):
        openai.api_key = key
        self.embeddingModel = embeddingModel
        self.completionModel = completionModel

    # generateQuestions function used by `prepare`
    # https://github.com/openai/openai-cookbook/blob/main/techniques_to_improve_reliability.md
    def generateQuestions(self, answer, numQuestions=3):
        questions = []
        for i in range(numQuestions):
            response = openai.ChatCompletion.create(
                model=self.completionModel,
                messages=[
                    self.generatePrompt(
                        answer, 'io/prompts/generateQuestionsPerson.prompt.txt')
                ]
            )
            questions.append(response['choices'][0]['text'])

    # embeds a single sentence
    # TODO: consider embedding multiple sentences at once

    def embedSentence(self, text):
        text = text.replace("\n", " ")  # question: Do i need this line?
        response = openai.Embedding.create(
            input=[text],
            model=self.embeddingModel,
        )
        return response

    # searches for the most similar embedding
    # returns the embedding index
    def searchEmbeddings(self, df, question):
        # embed the question
        questionEmbedding = self.embedSentence(
            question)
        # find the most similar sentence
        maxSimilarity = 0
        maxSimilarityIndex = 0
        for i, embedding in enumerate(df.embeddings):
            # similarity = cosineSimilarity(
            #     np.array(questionEmbedding['data'][0]['embedding']), embedding)
            similarity = cosine_similarity(
                embedding, questionEmbedding['data'][0]['embedding'])
            if (similarity) > 0.868500:
                print(f"{i}: {similarity} - {df.iloc[i].sentences}")
            if similarity > maxSimilarity:
                maxSimilarity = similarity
                maxSimilarityIndex = i
        # return the most similar sentence index
        # return maxSimilarityIndex
        # return the most similar embedding
        return df.iloc[maxSimilarityIndex].sentences


openaiClient = OpenAIClient(os.environ['OPENAI_KEY'])
