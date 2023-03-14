import os
from commons.Configs import configs
from commons.File import file
import openai


class OpenAIClient:
    def __init__(self, debug=False):
        self.debug = debug
        openai.api_key = configs.OPENAI_KEY

    def buildPrompt(self, name, variables):
        promptFilePath = os.path.join(configs.promptsDir, f"{name}.prompt.txt")
        prompt = file.readFile(promptFilePath)
        for key, value in variables.items():
            prompt = prompt.replace(f"{{{key}}}", value)
        return prompt

    def generateSyntheticQuestions(self, prompt):
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
        questionAnswers = [x.split("(A)") for x in responseText.split("\n")]
        questionAnswers = [row for row in questionAnswers if len(row) >= 2]
        # ----------------------------------------------
        # debug
        if self.debug:
            for x in questionAnswers:
                print("Q: ", x[0])
                print("A: ", x[1])
        # ----------------------------------------------
        return [{"question": x[0], "answer": x[1]} for x in questionAnswers]


openaiClient = OpenAIClient()
