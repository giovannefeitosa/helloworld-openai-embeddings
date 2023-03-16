import json

text = """
Intent: Background

Questions:
* Where was Pelé born?
* Which state in Brazil is Pelé's birthplace?
* When was Pelé born?
* Is there a street named after Pelé in his birthplace?
* Is there a statue of Pelé in Três Corações?

Answers:
Pelé was born in Três Corações, which is located in the state of Minas Gerais, Brazil in 1940. Rua Edson Arantes do Nascimento, a street named after him, is located in the city of Três Corações. Additionally, a statue of Pelé can be found near the downtown in Três Corações.

Intent: Realname

Questions:
* What is the full name of Pelé?
* How is the name of Pelé?
* What is the name of Pelé?
* What is the birth name of Pelé?
* What's the real name of Pelé?

Answers:
Pelé's real name is Edson Arantes do Nascimento.

Intent: Work

Questions:
* What did Pelé do for a living?
* What was Pelés occupation?
* Was football player his official job?

Answers:
Pelé was a Brazilian football player, it was his full-time occupation.

Intent: Highscore

Questions:
* How many goals did Pelé score in his whole career?
* How much goals did Pelè score altogether?
* How many goals did Edson Arantes do Nascimento score?
* The count of goals scored by Pele?

Answers:
Pelé scored 1,279 goals throughout his entire career, which is recognized as a Guinness World Record.
"""


def parseResponse(text):
    lines = text.strip().split('\n')
    result = []
    current_intent = None
    for i, line in enumerate(lines):
        if line.lower().startswith('intent'):
            current_intent = {'intent': line.split(
                ':')[1].strip(), 'questions': [], 'answer': ''}
            result.append(current_intent)
        elif line.startswith('*'):
            question = line[1:].strip()
            current_intent['questions'].append(question)
        elif line.lower().startswith('answer'):
            answer = line.split(':')[1].strip()
            if answer == "" and i < len(lines) - 1:
                answer = lines[i + 1].strip()
            current_intent['answer'] = answer
    return result


parsed = parseResponse(text)
print(json.dumps(parsed, indent=2))
