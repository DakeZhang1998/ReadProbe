import streamlit as st

import modules


# Some global parameters
top_n = 3  # Top n search results from Bing will be used to generate answers.
n_questions = 3  # The number of questions that ChatGPT needs to come up with.


if 'generated' not in st.session_state:
    st.session_state.generated = 0
for i in range(top_n):
    if f'question_{i}_feedback' not in st.session_state:
        st.session_state[f'question_{i}_feedback'] = 0


# Building the main page
st.markdown('# ReadProbe')
st.markdown('A tool to support lateral reading.')

input_text = st.text_area('Help me probe into:', 'Demo')

col1, _, _, _, _, col6 = st.columns(6)
with col1:
    probe_button = st.button(':mag: &nbsp; Probe')
with col6:
    refresh_button = st.button(':arrows_counterclockwise: &nbsp; Refresh')

if refresh_button:
    if 'generated' in st.session_state:
        st.session_state.generated = 0
    for i in range(top_n):
        if f'question_{i}_feedback' in st.session_state:
            st.session_state[f'question_{i}_feedback'] = 0
    st.cache_data.clear()

if probe_button or st.session_state.generated == 1:
    if input_text == 'Please copy and paste the text you want to probe into.':
        st.warning('Please input your text.')
    else:
        with st.spinner('Generating questions ...'):
            questions = modules.generate_questions(input_text)
        for i, question in enumerate(questions):
            with st.expander(f'**{i + 1}\. {question}**', expanded=True):
                with st.spinner('Searching online ...'):
                    search_result = modules.bing_search(question, top_n=top_n)
                with st.spinner('Generating answers ...'):
                    st.markdown(f'> {modules.summarize(question, " ".join([doc for url, doc in search_result]))}')
                for j in range(len(search_result)):
                    st.markdown(f'{j + 1}. {search_result[j][0]}')
                button = st.button(':thumbsup:  &nbsp; I like this one', key=f'thumbsup_for_q{i+1}')
                if button or st.session_state[f'question_{i}_feedback'] == 1:
                    st.session_state[f'question_{i}_feedback'] = 1
                    st.info('Thanks for your feedback!')
    st.session_state.generated = 1

