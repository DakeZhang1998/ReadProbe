# ReadProbe

## Features

## Plans
- [ ] Bing search function: Given a question, 
this function should return a string which is the concatenation of the web
documents of top **3** Bing search results.
- [ ] Question generation function: Given a piece of text, this function
should call ChatGPT APIs to generate a list questions relevant to the text
to support lateral reading.
- [ ] Answer generation function: Given a generated question and top **n**
relevant documents found by Bing search, this function should call ChatGPT
APIs to generate an answer to the question.
- [ ] Input text examination. To avoid intentionally malicious input,
we should filter out certain black-list words and check the language 
(English only).
- [ ] For each generated question, there should be a "like" button so that
users can indicate if they like the generated questions.
- [ ] Ask friends to try this web app and provide feedback.
- [ ] Make sure the API key is provided in the cloud app, not in this repo.
- [ ] Log histories (input, output, feedback) into a online database.

## Q&A
1. How to run this project on my local machine? \
Make sure you have [Streamlit](https://streamlit.io/) installed. 
Then run this command in the root repository of this project 
`streamlit run main.py`. 
2. 