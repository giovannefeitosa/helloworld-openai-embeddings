# Roadmap

## [Done] Step 1: Setup environment

Things to consider when making the project structure:

- [x] The project should have isolated dependencies (I will use pip's `venv`)
- [x] The project structure should be well organized
- [ ] The project should have a demo webpage
- [x] The project should be easy to manage through the terminal
- [x] We should have a private `.env` file so we don't leak OpenAI's API key
- [x] Do not leak original sample text

## [Done] Step 2: Break the content into sequences

Read more:
[Breaking a text into sequences](https://giovannefeitosa.notion.site/Breaking-a-text-into-sequences-4a453b09ee224ead8323fd3981216cfb)

## [Done] Step 3: Create initial test with OpenAI's API

I tried the following:

1. Process sentences with the Embeddings API
2. Calculate the cosine similarity between the question and the embeddings

This test failed because the answers were not good enough.

Conclusion: Comparing the question with the most similar embeddings does not return good answers.
            The most similar phrase is not necessarily the answer.

## [Done] SPIKE:

In order to improve the answers, it's useful to refer to the official docs and examples.

I took some time to read the docs (again) and the examples in the 
[OpenAI Cookbook repository](https://github.com/openai/openai-cookbook/).

The most interesting example I found is the 
[Question Answering using Embeddings](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb).

What I've learnt:

- We can use OpenAI completion API to generate synthetic data and augment our dataset
- We can use any kind of machine learning algorithm to train a model that can answer questions
- It's a good practice to label the data before doing any kind of calculation
- It's a good practice to use completions API to generate synthetic data and augment our dataset

## [Done] Replanning

- [x] Create a command to transform a txt file into a dataset with questions and answers.<br/>
      Command: `bash manage.sh prepare <txt_file>`.

- [x] Create a command to train a model that answers questions based in the dataset file<br/>
      Command: `bash manage.sh train`

- [x] Create a command to answer questions based on the trained model<br/>
      Command: `bash manage.sh ask "<question>"`

- [ ] Create a command to run a demo webserver where we can ask questions<br/>
      Command: `bash manage.sh serve <model_file>`

## [Done] Create command: `prepare`

For the preparation, we should follow this steps:

* Read the text file
* Split text into sentences
* Use OpenAI completion API to generate synthetic questions for each sentence
* Save the questions and the answers in a jsonl file

I've created this file: `io/prompts/generateQuestionsPerson.prompt.txt` that is meant to be used with the OpenAI completion API.
To generate questions for each sentence in the input text.

This prompt was based in [this doc](https://github.com/openai/openai-cookbook/blob/main/techniques_to_improve_reliability.md)

I use `gpt-3.5-turbo` as the model. Because [here](https://platform.openai.com/docs/guides/chat/chat-vs-completions)
it says:

> Because `gpt-3.5-turbo` performs at a similar capability 
> to `text-davinci-003` but at 10% the price per token, 
> we recommend `gpt-3.5-turbo` for most use cases.

TODO: Read this amazing paper about a stunning technique called `STaR: Self-Taught Reasoner`.<br/>
      [Paper](https://arxiv.org/pdf/2203.14465.pdf).

- [x] (dataset file) Generate a json file with questions and answers based in the text
- [x] (embeddings file) Generate a embeddings file based in the dataset file

## [Done] Create command: `ask`

For answering a single question.

I can use this command to try different prompts and strategies to answer questions.

## [WIP] Create command: `train`

For the training, we should follow this steps:

* Read the jsonl file
* Train a model that can answer questions based on the jsonl file
  TODO: I need to decide which strategy I will use to train the model.
* Save the model in a file

## [WIP] Create command: `serve`

For the serving, we should follow this steps:

* Read the model file
* Create a [Gradio](https://www.gradio.app/) webserver
* Print the browser url in the terminal
