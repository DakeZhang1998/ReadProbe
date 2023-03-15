import streamlit as st

import modules


st.markdown('# ReadProbe')
st.markdown('A tool to support lateral reading.')

input_text = st.text_area('Help me probe into:', 'Please copy and paste the text you want to probe into.')

if st.button('Probe'):
    if input_text == 'Please copy and paste the text you want to probe into.':
        st.warning('Please input your text.')
    else:
        with st.spinner('Generating questions ...'):
            questions = modules.generate_questions(input_text)
        with st.spinner('Searching online ...'):
            search_result = modules.bing_search(questions, top_n=3)
        with st.spinner('Generating answers ...'):
            for i, question in enumerate(questions):
                st.markdown(f'{i + 1}. {question}')
                st.markdown(modules.summarize(question, ' '.join([doc for url, doc in search_result[i]])))
                for j in range(len(search_result[0])):
                    st.markdown(f'\t{j + 1}. {search_result[i][j][0]}')
