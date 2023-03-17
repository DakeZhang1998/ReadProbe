import uuid
import json
import streamlit as st

import modules


# Some global parameters
top_n = 3  # Top n search results from Bing will be used to generate answers.
n_questions = 3  # The number of questions that ChatGPT needs to come up with.
enable_logging = True  # Turn on or off whether to log user feedback to Google Forms.


if 'generated' not in st.session_state:
    st.session_state.generated = 0
if 'generation_id' not in st.session_state:
    st.session_state.generation_id = uuid.uuid4()
for i in range(top_n):
    if f'question_{i}_feedback' not in st.session_state:
        st.session_state[f'question_{i}_feedback'] = 0


# Building the main page
st.markdown('# :bulb: ReadProbe')
st.markdown('A tool to support lateral reading.')

demo = 'President Joe Biden recently released his budget proposal. The president is required by law to submit a ' \
       'request to Congress prior to the start of a new fiscal year. Ultimately, what’s passed will be dictated by ' \
       'Congress. The president’s budget request has become more of a wish list that plays a role in setting the ' \
       'temperature for the policy battles to come on Capitol Hill and in the regulatory agencies. Sadly, ' \
       'Biden’s budget contained a series of tax hikes that would batter the American economy.'

input_text = st.text_area('Help me probe into:', demo)

col1, col2 = st.columns(2)
with col1:
    probe_button = st.button(':mag: &nbsp; Probe')
with col2:
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
                    st.info('Thanks for your feedback!')
                    if button or st.session_state[f'question_{i}_feedback'] == 0 and enable_logging:
                        modules.log_data(log_id=str(st.session_state.generation_id), user_input=input_text,
                                         output=json.dumps(record), action='thumbsup')
                    st.session_state[f'question_{i}_feedback'] = 1
            records.append(record)
    if probe_button and st.session_state.generated == 0 and enable_logging:
        modules.log_data(log_id=str(st.session_state.generation_id), user_input=input_text, output=json.dumps(records),
                         action='generation')
    st.session_state.generated = 1


# Layout for the sidebar
with st.sidebar:
    st.markdown('# :information_source: User Info')
    st.markdown('### What is lateral reading?')
    st.markdown('Lateral reading is a critical thinking approach used to evaluate the credibility and accuracy of '
                'information found online by stepping away from the initial source and exploring other sources to '
                'verify its authenticity.')
    st.markdown('### How can lateral reading help fight online misinformation?')
    st.markdown('Lateral reading can reduce the risk of being misled by misinformation, propaganda, and other forms '
                'of disinformation. By cross-referencing information with multiple sources, users can become more '
                'informed and responsible consumers of information, promoting a better online community.')
    st.markdown('### How does this tool support lateral reading?')
    st.markdown('All you need is to copy and paste a text into the input box and then click on the "Probe" '
                'button. This tool (powered by [OpenAI](https://openai.com/)) will generate **three** '
                'questions you may want to ask and provide answers by summarizing relevant documents found by [Bing]('
                'https://bing.com/). You can give feedback on the generated contents. The generation time depends on '
                'responsiveness of API calls. Please wait till the generation completes '
                'before interacting with the page.')
