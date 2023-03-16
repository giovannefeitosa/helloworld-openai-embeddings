import os
from commons.File import file
from commons.Configs import configs


class PromptUtils:
    def parseResponseText(self, text):
        lines = text.strip().split('\n')
        result = []
        current_intent = None
        for line in lines:
            if line.startswith('intent:'):
                current_intent = {'intent': line.split(
                    ':')[1].strip(), 'questions': [], 'answer': ''}
                result.append(current_intent)
            elif line.startswith('*'):
                question = line[1:].strip()
                current_intent['questions'].append(question)
            elif line.startswith('answer:'):
                answer = line.split(':')[1].strip()
                current_intent['answer'] = answer
        return result

    def buildPrompt(self, name, variables):
        promptFilePath = os.path.join(configs.promptsDir, f"{name}.prompt.txt")
        promptVariables = configs.getPromptVariables(variables)
        try:
            prompt = file.readFile(promptFilePath)
        except:
            print("Error: prompt not found: ", promptFilePath)
            exit(1)
        for key, value in promptVariables.items():
            prompt = prompt.replace(f"{{{key}}}", value)
        try:
            assert prompt.count("{") == 0
        except AssertionError:
            print("Error: unresolved variables in prompt: ", prompt)
            exit(1)
        return prompt


promptUtils = PromptUtils()
