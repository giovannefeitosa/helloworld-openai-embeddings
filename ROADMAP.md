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

### [Done] Replanning

- [ ] Create a command to transform a txt file into something we can work with.
      Command: `bash manage.sh prepare <txt_file> <output_jsonl_file>`.
      I will use the same jsonl format [described here](https://platform.openai.com/docs/guides/fine-tuning)

- [ ] Create a command to train a model that answers questions based in the jsonl file
      Command: `bash manage.sh train <jsonl_file> <output_model_file>`

- [ ] Create a command to answer questions based on the trained model
      Command: `bash manage.sh answer <model_file> <question>`

- [ ] Create a command to run a demo webserver where we can ask questions
      Command: `bash manage.sh serve <model_file>`

TODO: I need to decide which strategy I will use to train the model.
