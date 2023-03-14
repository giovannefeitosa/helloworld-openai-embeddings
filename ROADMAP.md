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

## [WIP] Step 3: Process sentences with the Embeddings API

I just finished doing a successful test with the Embeddings API.

I've decided that after getting the embeddings, I will save them to a file.
So I don't need to call the API every time I want to use the embeddings.

This allows us to avoid unecessary API calls.

### TODO:

- [ ] Load the embeddings from a file
- [ ] If the embeddings file doesn't exist,
      then get the embeddings from the API and save the results to a file
- [ ] Create a notion page to explain 
      how to create embeddings using the API

## [TODO] Step 4: Get input questions and find the answers

(doing a search through the embeddings)
