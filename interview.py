import streamlit as st
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage, SystemMessage

# Load API key
load_dotenv()

# Load system prompt from file
with open("InterviewerLLMPrompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

# Example tech stack + variables
TECH_STACK = ["Python", "Streamlit", "LangChain", "Anthropic Claude"]
YOE = 3  # years of experience
POS = "Machine Learning Engineer"

# Initialize LLM
llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)

# Streamlit page config
st.set_page_config(page_title="Tech Stack Interview Bot", page_icon="🤖")
st.title("🤖 Tech Stack Interview Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]
if "step" not in st.session_state:
    st.session_state.step = 0
if "active" not in st.session_state:
    st.session_state.active = False
if "done" not in st.session_state:
    st.session_state.done = False

# Chat display
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User input
if not st.session_state.done:
    user_input = st.chat_input("Type START to begin, or EXIT to quit...")

    if user_input:

        # Show user's message immediately
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)


        # Handle EXIT
        if user_input.strip().upper() == "EXIT":
            with st.chat_message("assistant"):
                st.markdown("Thank you! Terminating the interview.")
            st.session_state.done = True

        # Handle START
        elif user_input.strip().upper() == "START" and not st.session_state.active:
            st.session_state.active = True
            st.session_state.step = 1

            # Generate first question
            with st.spinner("Generating first question..."):
                response = llm.invoke(st.session_state.messages + [
                    HumanMessage(content=f"Tech stack: {TECH_STACK}, YOE: {YOE}, POS: {POS}. Start the Q&A. Ask the first question.")
                ])
            st.session_state.messages.append(HumanMessage(content=user_input))
            st.session_state.messages.append(response)

            with st.chat_message("assistant"):
                st.markdown(response.content)

        # Handle Q&A flow
        elif st.session_state.active and st.session_state.step <= 5:
            st.session_state.messages.append(HumanMessage(content=user_input))

            if st.session_state.step == 5:
                # Last question answered → Thank you
                with st.chat_message("assistant"):
                    st.markdown("✅ Thank you for your responses. Interview complete!")
                st.session_state.done = True
            else:
                # Continue with next question
                with st.spinner("Generating next question..."):
                    response = llm.invoke(st.session_state.messages + [
                        HumanMessage(content=f"Continue the interview. Ask question {st.session_state.step+1} of 5.")
                    ])
                st.session_state.messages.append(response)
                st.session_state.step += 1

                with st.chat_message("assistant"):
                    st.markdown(response.content)
