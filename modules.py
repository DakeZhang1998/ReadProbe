import openai
import requests
import streamlit as st
from typing import List
from bs4 import BeautifulSoup


@st.cache_data(show_spinner=False)
def bing_search(query, top_n=3):
    # This function takes as input a query and
    # return a list containing Bing search results (top n) for the query.
    headers = {'Ocp-Apim-Subscription-Key': st.secrets.azure_bing_keys.key}
    return_list = []
    response = requests.get('https://api.bing.microsoft.com/v7.0/search', headers=headers,
                            params={'q': query, 'textDecorations': True, 'textFormat': "HTML"})
    response.raise_for_status()
    search_results = response.json()
    for result in search_results['webPages']['value'][:top_n]:
        result_response = requests.get(result['url'])
        soup = BeautifulSoup(result_response.content, 'html.parser')
        text = soup.find('body').get_text()
        clean_text = ''
        for line in text.split('\n'):
            clean_line = line.strip()
            if len(clean_line.split(' ')) > 3:
                clean_text += f'{clean_line}\n'
        return_list.append([result['url'], clean_text])
    return return_list


@st.cache_data(show_spinner=False)
def generate_questions(input_text: str):
    # This function calls OpenAI APIs to generate a list of questions
    # based on the input text given by the user.
    return ['What is ReadProbe?', 'How should I use ReadProbe?', 'How does ReadProbe work?']


@st.cache_data(show_spinner=False)
def summarize(question: str, document: str):
    # This function takes as input a pair of question and document to produce
    # a short summary to answer the question using the information in the document.
    return 'Summary produced by ChatGPT.'


# @st.cache_data(show_spinner=False)
# def log_data(action: str):
#     # This function takes as input a pair of question and document to produce
#     # a short summary to answer the question using the information in the document.
#     st.balloons()


if __name__ == '__main__':
    # This part is used for testing functions in this file.
    results = bing_search('hello?')
    print('here')
