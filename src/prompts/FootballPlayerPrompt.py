from commons.OpenAIClient import openaiClient
from commons.PromptUtils import promptUtils
import traceback


class FootballPlayerPrompt:
    def __init__(self, extraData={}):
        self.extraData = extraData

    def retrieveTopics(self):
        # parse the prompt file
        promptText = promptUtils.buildPrompt(
            'paragraph', self.extraData)
        # parse the header prompt file
        # promptHeaderText = promptUtils.buildPrompt(
        #    'header', self.extraData)
        # generate the synthetic questions
        response = openaiClient.generateSyntheticQuestions(
            prompt=promptText,
            # header=promptHeaderText,
            temperature=1.3,        # default 1    better 1.3
            presence_penalty=-0.85,    # default 0    better -1
            frequency_penalty=0,  # default 0    better 0
            max_tokens=1300,
        )
        return self.parseResponseText(response['choices'][0]['message']['content'])

    def parseResponseText(self, responseText):
        """ Example Response
        ,,,
        """
        try:
            responseArray = f"Topic: {responseText}".split("\n")
            result = []
            currentDict = {}
            for i, row in enumerate(responseArray):
                rowLower = row.lower()
                if rowLower.startswith("topic"):
                    currentDict = {
                        "topic": "",
                        "questions": [],
                        "answer": ""
                    }
                    currentDict['topic'] = row.split(":", 1)[1].strip()
                elif rowLower.startswith("*"):
                    currentDict['questions'].append(
                        row.split("*", 1)[1].strip())
                elif rowLower.startswith("answer"):
                    currentDict['answer'] = row.split(":", 1)
                    if len(currentDict['answer']) > 1:
                        currentDict['answer'] = currentDict['answer'][1].strip()
                    else:
                        currentDict['answer'] = currentDict['answer'][0] \
                            .replace('Answer', '').replace('answer', '').strip()
                    if currentDict['answer'] == "":
                        currentDict['answer'] = responseArray[i+1]
                    currentDict['answer'] = currentDict['answer'].replace(
                        '*', '').strip()
                    result.append(currentDict)
            return result
        except Exception as e:
            print(responseText)
            print("")
            print('\n\nError:\n')
            print(e)
            # print error stack
            traceback.print_exc()
            exit(1)
