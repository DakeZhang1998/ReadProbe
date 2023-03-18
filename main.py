import uuid
import json
import streamlit as st
from langdetect import detect

import modules

# Some global parameters
top_n = 3  # Top n search results from Bing will be used to generate answers.
n_questions = 5  # The number of questions that ChatGPT needs to come up with.
enable_logging = True  # Turn on or off whether to log user feedback to Google Forms.

if 'generated' not in st.session_state:
    st.session_state.generated = 0
if 'generation_id' not in st.session_state:
    st.session_state.generation_id = uuid.uuid4()
for i in range(n_questions):
    if f'question_{i}_feedback' not in st.session_state:
        st.session_state[f'question_{i}_feedback'] = 0

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
                'button. This tool (powered by [OpenAI](https://openai.com/)) will generate **five** '
                'questions you may want to ask and provide answers by summarizing relevant documents found by [Bing]('
                'https://bing.com/). You can give feedback on the generated contents. The generation time depends on '
                'responsiveness of API calls. Please wait till the generation completes '
                'before interacting with the page.')

# Building the main page
st.markdown('# :bulb: ReadProbe [![GitHub-link](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo='
            'github&logoColor=white)](https://github.com/DakeZhang1998/ReadProbe)')
st.markdown('An AI-powered tool to support **lateral reading**.')
st.markdown('### :pushpin: Instruction')
st.markdown('Please read the information on the left before using this tool. Your input should contain at least 10 '
            'words for generating meaningful questions and at most 2000 words due to the limit of ChatGPT.')
st.markdown('### :robot_face: Start Here')
demo = 'Demo:\n' \
       'Elon Musk\'s account was briefly suspended by an outgoing Twitter employee.'

input_text = st.text_area(label='Help me probe into:', value=demo, height=130)

col1, col2 = st.columns(2)
with col1:
    probe_button = st.button(':mag: &nbsp; Probe')
with col2:
    refresh_button = st.button(':arrows_counterclockwise: &nbsp; Reset')

if refresh_button:
    modules.refresh(top_n=top_n)

# Interations
if probe_button or st.session_state.generated == 1:
    if probe_button and st.session_state.generated == 1:
        modules.refresh(top_n=top_n)
    if len(input_text.strip()) == 0:
        st.warning('Please input your text.')
        st.stop()
    else:
        # Input Check
        with st.spinner('Checking input ...'):
            if detect(input_text) != 'en':
                st.warning('Only English is supported for now. Please try another input.')
                st.stop()
            if not modules.input_check(input_text):
                st.warning('Your input may contain harmful content. Please try another input.')
                st.stop()
            if len(input_text.split()) < 10:
                st.warning('Your input is too short. Please try longer input.')
                st.stop()
            if len(input_text.split()) > 2000:
                st.warning('Your input is too long. Please try shorter input.')
                st.stop()

        # Generate questions
        with st.spinner('Generating questions ...'):
            questions = modules.generate_questions(input_text)

        # Search online and generate answers
        records = []
        for i, question in enumerate(questions):
            record = [question]
            with st.expander(f'**{i + 1}\. {question}**', expanded=True):
                with st.spinner('Searching online ...'):
                    search_result = modules.bing_search(question, top_n=top_n)
                with st.spinner('Generating answers ...'):
                    record.append([url for url, doc in search_result])
                    answer = modules.summarize(question, ' '.join([doc for url, doc in search_result]))
                    answer = str(answer).replace('$', '\\$')
                    record.append(answer)
                    st.markdown(f'> {answer}')
                for j in range(len(search_result)):
                    st.markdown(f'{j + 1}. {search_result[j][0]}')
                button = st.button(':thumbsup:  &nbsp; I like this one', key=f'thumbsup_for_q{i + 1}')
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

st.markdown('### :warning: Disclaimer')
st.markdown('Content generation in this web application is performed mainly by calling '
            'OpenAI APIs and Bing APIs. Even though we perform some processing to '
            'improve the quality of the generated content, due to our limited knowledge of '
            'the models behind those services, we can not make sure the generated '
            'content won\'t contain biased, unethical, incorrect, or controversial '
            'information. Please be aware of the potential risks of using this tool. '
            '**The content generated here doesn\'t represent the opinions of the '
            'developers in this project.** If you notice potentially malicious content generated by this app, '
            'please open an [issue](https://github.com/DakeZhang1998/ReadProbe/issues) '
            'to report. Your valuable feedback is deeply appreciated.')
