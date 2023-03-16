# RESULTS

I will track my results here.

## Artifacts

* [Online demo](https://huggingface.co/spaces/giovannefeitosa/chatbot-pele)
* [Blog posts](https://giovannefeitosa.notion.site/Prompt-Engineering-6e90fa41112642cbbdcca6158da7a0ff)

## Technologies

* [Spacy](https://spacy.io/) - 
  For splitting the text into sentences.
* [OpenAI Chat Completions](https://platform.openai.com/docs/guides/chat) - 
  For generating synthetic questions.
* [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) - 
  For embedding the sentences.
* [Jupyter Notebook](https://jupyter.org/) - 
  For creating the training notebook and try different strategies.
* [Scikit-learn](https://scikit-learn.org/stable/) -
  For training a simple neural network that can answer questions.
* [Gradio](https://www.gradio.app/) - 
  For creating a demo webserver.
* [Hugging Face](https://huggingface.co/) - 
  For publishing an online demo

## Trials

More details in [Roadmap](./ROADMAP.md).


### Try 1 - naive approach

I tried to compare the question embedding against the sentences embeddings and then find the closest match using cosine similarity.

Results: The results were bad.

Action: Use openai completion API to summarize the sentences.

### Try 2 - generate synthetic questions

I tried to generate synthetic questions and compared the embeddings of the synthetic questions against the question embeddings.

I tried different prompts.

Results: The results were bad.

Action: Create a neural network to select the best answer.

### Try 3 - Train a neural network

Created a demo training at [src/train.ipynb](./src/train.ipynb) using sklearn.

Created `bash manage.sh train` command to train the model.

Results: It worked!

### Try 4 - Test prompts inspired by Rasa NLU

I tried to generate intents and multiple questions for a single answer. Because I could spend less tokens and I could generate more questions.

Results: It worked! But now the quality of questions is worse.

#### Wierd results

> topic: deathdate
> Question: When did Pelé pass away?
> The given text lists a future date (29 December 2022), so Pelé has not passed away yet as of October 2021.

After this wierd result I added this to the prompt: `Today is {TODAY}` ([did it worked?]()).

