import openai
import logging
import requests
import streamlit as st
from bs4 import BeautifulSoup


openai.api_key = st.secrets.openai_keys.key


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
    for result in search_results['webPages']['value']:
        result_response = requests.get(result['url'])
        try:
            soup = BeautifulSoup(result_response.content, 'html.parser')
            text = soup.find('body').get_text()
            clean_text = ''
            for line in text.split('\n'):
                clean_line = line.strip()
                if len(clean_line.split(' ')) > 3:
                    clean_text += f'{clean_line}\n'
        except AttributeError as e:
            print(f'[INFO] Skipped one URL [{result["url"]}] with error {e}.')
            continue
        return_list.append([result['url'], clean_text])
        if len(return_list) > top_n:
            break
    return return_list


@st.cache_data(show_spinner=False)
def generate_questions(input_text: str):
    # This function calls OpenAI APIs to generate a list of questions
    # based on the input text given by the user.
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are an AI assistant to help users perform the task of lateral reading. '
                                          'You will be given a piece of text. Your task is to raise atomic, simple, '
                                          'factoid questions that users may ask when reading the text. The questions '
                                          'should not be too complicated and should be suitable to be used as queries '
                                          'to a search engine like Bing. Your questions will motivate users to search '
                                          'for relevant documents to better understand the given text.'},
            {'role': 'user', 'content': f'{input_text}\n------\n'
                                        f'Please come up with the three most critical background questions.'}
        ],
        temperature=0.8,
    )
    response = completion['choices'][0]['message']['content']
    questions = []
    for line in response.split('\n'):
        question = line.strip()
        if len(question) > 5:
            questions.append(question[3:])
    return questions


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
    results = generate_questions('The US Coast Guard has failed to use its power to prevent and punish sexual assault '
                                 'and misconduct for decades — despite growing evidence that this kind of behavior is '
                                 'a longstanding problem at sea.')
    print('here')
