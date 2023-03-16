# helloworld-openai-embeddings

The goal of this project is to create a question answering demo using OpenAI embeddings and a sample text.

For more information, please read the [project roadmap](docs/ROADMAP.md) and the [solution proposal](docs/RESULTS.md).

## Requirements

* Unix (Ubuntu, WSL 2, etc.)
* Python  >  3
* Pip     >= 22
* Venv    >  3

You should already have these dependencies installed.

## Install

Install the python dependencies:

```
bash manage.sh install
```

## Prepare

Generate synthetic questions and embeddings:

```
bash manage.sh prepare "io/data/sample.txt"
```

> Note: You must pass the path to a text file as the first argument.

## Train

Train a model to answer questions:

```
bash manage.sh train
```

## Ask

Ask a question through the command line:

```
bash manage.sh ask "What is the name of the main character?"
```

> Note: Please use double quotes to pass the question.

## Demo webserver

Start a demo webserver:

```
bash manage.sh serve
```
