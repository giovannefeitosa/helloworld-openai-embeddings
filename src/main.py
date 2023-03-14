# this is the entrypoint for the application
from embeddings import loadEmbeddings
from OpenAIClient import openaiClient

# a list of embeddings that we will use to compare the question
df = loadEmbeddings()

# the question that we want to find the answer for
question = "How many goals did Pelé score in his career?"

result = openaiClient.searchEmbeddings(df, question)

print(f"Question: {question}")
print(f"Answer: {result}")
