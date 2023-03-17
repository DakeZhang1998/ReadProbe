import uuid
import json
import streamlit as st

import modules


# Some global parameters
top_n = 3  # Top n search results from Bing will be used to generate answers.
n_questions = 3  # The number of questions that ChatGPT needs to come up with.


if 'generated' not in st.session_state:
    st.session_state.generated = 0
if 'generation_id' not in st.session_state:
    st.session_state.generation_id = uuid.uuid4()
for i in range(top_n):
    if f'question_{i}_feedback' not in st.session_state:
        st.session_state[f'question_{i}_feedback'] = 0


# Building the main page
st.markdown('# ReadProbe')
st.markdown('A tool to support lateral reading.')

demo = 'President Joe Biden recently released his budget proposal. The president is required by law to submit a ' \
       'request to Congress prior to the start of a new fiscal year. Ultimately, what’s passed will be dictated by ' \
       'Congress. The president’s budget request has become more of a wish list that plays a role in setting the ' \
       'temperature for the policy battles to come on Capitol Hill and in the regulatory agencies. Sadly, ' \
       'Biden’s budget contained a series of tax hikes that would batter the American economy.'

input_text = st.text_area('Help me probe into:', demo)

col1, _, _, _, _, col6 = st.columns(6)
with col1:
    probe_button = st.button(':mag: &nbsp; Probe')
with col6:
    refresh_button = st.button(':arrows_counterclockwise: &nbsp; Refresh')


if refresh_button:
    modules.refresh(top_n=top_n)


if probe_button or st.session_state.generated == 1:
    if probe_button and st.session_state.generated == 1:
        modules.refresh(top_n=top_n)
    if len(input_text.strip()) == 0:
        st.warning('Please input your text.')
    else:
        with st.spinner('Generating questions ...'):
            questions = modules.generate_questions(input_text)
        records = []
        for i, question in enumerate(questions):
            record = [question]
            with st.expander(f'**{i + 1}\. {question}**', expanded=True):
                with st.spinner('Searching online ...'):
                    search_result = modules.bing_search(question, top_n=top_n)
                with st.spinner('Generating answers ...'):
                    record.append([url for url, doc in search_result])
                    answer = modules.summarize(question, ' '.join([doc for url, doc in search_result]))
                    record.append(answer)
                    st.markdown(f'> {answer}')
                for j in range(len(search_result)):
                    st.markdown(f'{j + 1}. {search_result[j][0]}')
                button = st.button(':thumbsup:  &nbsp; I like this one', key=f'thumbsup_for_q{i+1}')
                if button or st.session_state[f'question_{i}_feedback'] == 1:
                    st.session_state[f'question_{i}_feedback'] = 1
                    st.info('Thanks for your feedback!')
                    modules.log_data(log_id=str(st.session_state.generation_id), user_input=input_text,
                                     output=json.dumps(record), action='thumbsup')
            records.append(record)
    st.session_state.generated = 1
    modules.log_data(log_id=str(st.session_state.generation_id), user_input=input_text, output=json.dumps(records),
                     action='generation')

