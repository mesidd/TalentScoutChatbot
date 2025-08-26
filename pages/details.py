import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

#****************************** Set-up LLM and Utility Function ********************************
load_dotenv()
chat_model = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')

def get_llm_reply(user_answer, next_question):
    """Pass user answer + next question to LLM and return formatted reply."""
    prompt = (
        "You are a polite and friendly assistant collecting details for an interview.\n\n"
        f"The user answered: {user_answer}\n\n"
        f"Now, ask them this next question in a natural, but formal conversational way: {next_question}"
    )
    response = chat_model.invoke(prompt)
    return response.content


#****************************** Set page config ***********************************************
st.set_page_config(page_title="Personal Details", layout="centered")


#***************************** Title and subtitle *********************************************
st.markdown('<p class="big-font">Kindly provide us with your details </p>', unsafe_allow_html=True)


#***************************** SESSION STATE SETUP ********************************************
if "message_history" not in st.session_state:
    st.session_state.message_history = []
if "question_index" not in st.session_state:
    st.session_state.question_index = 0  # Track which question we're on


#***************************** Set the Questions for Personal Details ************************
QUESTIONS = [
    "Please enter your Full Name",
    "Please enter your e-mail address",
    "Please enter your phone number",
    "Please enter Years of Experience you have in your desired field",
    "Please enter your desired position(s)",
    "Please enter the Tech Stack(s) you are familiar with. Note that your subsequent interview will based on the basis of your tech stack"
]    


#***************************** Initial Questionaire ********************************************
# Display chat history
for msg in st.session_state.message_history:
    st.chat_message(msg["role"]).write(msg["content"])

# If there are still questions left, ask the current one
if st.session_state.question_index < len(QUESTIONS):

    # Get user input
    if user_input := st.chat_input("Type your answer here..."):
        # Save user response
        st.session_state.message_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # Move to next question
        st.session_state.question_index += 1

    # Show the next question (if available)
    if st.session_state.question_index < len(QUESTIONS):
        next_question = QUESTIONS[st.session_state.question_index]
        llm_reply = get_llm_reply(user_input, next_question)
        st.session_state.message_history.append({"role": "assistant", "content": llm_reply})
        st.chat_message("assistant").write(llm_reply)

    # Last scenario - All questions asked
    if st.session_state.question_index == len(QUESTIONS):
        st.chat_message("assistant").write(" Thank you for answering all the questions! \n We will now move forward with the interview")


print (st.session_state.message_history)