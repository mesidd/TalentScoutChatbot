import streamlit as st

# Set page config
st.set_page_config(
    page_title="TalentScout Interview Chatbot",
    page_icon="👋",
    layout="centered"
)

# Title and subtitle
st.markdown('<p class="big-font">👋 Welcome </p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">I am an intelligent Hiring Assistant chatbot for <b>TalentScout</b>, a recruitment agency specializing in technology placements. </p>', unsafe_allow_html=True)
st.markdown('<p class="small-font"> Here, your interview will be conducted. You need to provide us with a few details and we can get started with it', unsafe_allow_html=True)


user_input = st.chat_input('Type here')