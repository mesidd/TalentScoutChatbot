import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from config import QUESTIONS

#****************************** Set-up LLM and Utility Function ********************************
load_dotenv()
chat_model = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')

def get_llm_reply(message_history, next_question):
    """
    Pass the entire chat history + the next question to the LLM
    and return a natural conversational reply.
    """
    # Convert Streamlit's history format into LangChain messages
    messages = [SystemMessage(content="You are a polite HR assistant collecting details for an interview. " \
                                                "Be cheerful and appreciative towards the user.")]
    for msg in message_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    # Add the instruction to move forward
    messages.append(HumanMessage(content=f"Now ask the next question in a natural but polite way: {next_question}"))

    # Invoke LLM
    response = chat_model.invoke(messages)
    return response.content


#****************************** Set page config ***********************************************
st.set_page_config(page_title="Personal Details", layout="centered")


#***************************** Title and subtitle *********************************************
st.markdown('<header class="big-font"><h2>Kindly provide us with your details </header>', unsafe_allow_html=True)


#***************************** SESSION STATE SETUP ********************************************
if "message_history" not in st.session_state:
    st.session_state.message_history = []
if "question_index" not in st.session_state:
    st.session_state.question_index = 0  # Track which question we're on



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
        llm_reply = get_llm_reply(st.session_state.message_history, next_question)
        st.session_state.message_history.append({"role": "assistant", "content": llm_reply})
        st.chat_message("assistant").write(llm_reply)

    # Last scenario - All questions asked
    if st.session_state.question_index == len(QUESTIONS):
        final_message = f" Thank you for answering all the questions! We will now move forward with the interview"
        st.chat_message("assistant").write(final_message)
        st.session_state.message_history.append({"role": "assistant", "content": final_message})

        # Show button to redirect
        if st.button("➡️ Go to Interview"):
            st.switch_page("pages/interview.py")


print (st.session_state.message_history)