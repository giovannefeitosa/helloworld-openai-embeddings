# Command:
#   bash manage.sh prompt
# --------------------------------------------------
# This command will make a test call to the OpenAI API.
#
import sys
from commons.Configs import configs
from commons.File import file
from prepareutils.Embeddings import embeddings
from commons.OpenAIClient import openaiClient
from commons.PromptUtils import promptUtils
from prompts.FootballPlayerPrompt import FootballPlayerPrompt
import json

if __name__ == "__main__":
    prompt = FootballPlayerPrompt({
        "PARAGRAPH": "Edson Arantes do Nascimento (23 October 1940 – 29 December 2022), better known by his nickname Pelé, was a Brazilian professional footballer who played as a forward. Widely regarded as one of the greatest players of all time, he was among the most successful and popular sports figures of the 20th century. In 1999, he was named Athlete of the Century by the International Olympic Committee and was included in the Time list of the 100 most important people of the 20th century. In 2000, Pelé was voted World Player of the Century by the International Federation of Football History & Statistics (IFFHS) and was one of the two joint winners of the FIFA Player of the Century. His 1,279 goals in 1,363 games, which includes friendlies, is recognised as a Guinness World Record."
    })
    intents = prompt.retrieveTopics()
    print(json.dumps(intents, indent=2))
