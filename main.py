import streamlit as st

import modules


st.markdown('# ReadProbe')
st.markdown('A tool to support lateral reading.')

input_text = st.text_area('Help me probe into:', 'Please copy and paste the text you want to probe into.')

if st.button('Probe'):
    if input_text == 'Please copy and paste the text you want to probe into.':
        st.warning('Please input your text.')
    else:
        st.write('Output from ChatGPT ...')


