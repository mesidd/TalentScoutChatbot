from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field, EmailStr
from config import QUESTIONS
import streamlit as st
import time

load_dotenv()

model = ChatAnthropic(model = 'claude-3-5-haiku-20241022')


def get_llm_reply(message_history, next_question):
    """
    Pass the entire chat history + the next question to the LLM
    and stream a natural conversational reply.
    """
    
    chat_model = model
    # Convert Streamlit's history format into LangChain messages
    messages = [SystemMessage(content="You are a polite HR assistant collecting details for an interview. "
                                      "Be cheerful and appreciative towards the user. "
                                      "Do not tell me about your thought process")]
    for msg in message_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    # Add the instruction to move forward
    messages.append(HumanMessage(content=f"Now ask the next question in a natural but polite way: {next_question}"))

    # Stream response
    response_text = ""
    with st.chat_message("assistant"):
        response_box = st.empty()   # placeholder to update token by token
        for chunk in chat_model.stream(messages):
            if chunk.content:
                response_text += chunk.content
                response_box.markdown(response_text)
    return response_text


def extract_data_from_session_state(message_history):

    class PersonalDetails(BaseModel):

        name: str = Field(description="Write down the full name of the user")
        email: EmailStr = Field(description="Write down the e-mail address of the user")
        number: str = Field(description="Write down the Phone Number of the User")
        location: str = Field(default="India", description="Write down the location mentioned by the User")
        positions: str = Field(description="Write down the desired positions mentioned by the user")
        experience: float = Field(description="Write down the experience of the user")
        techstack: list[str] = Field (default=None, description="Write down all the tech stacks mentioned by the user in a list")
    

    structured_model = model.with_structured_output(PersonalDetails)

    result = structured_model.invoke(message_history)

    return (result)

#****************************** Streaming Helper ***********************************************
def stream_llm_response(messages=None, fixed_text=None):
    """Stream response from LLM or stream a fixed text token-by-token."""
    response_placeholder = st.empty()
    full_response = ""

    if fixed_text:  # manual streaming for fixed messages
        for token in fixed_text.split():
            full_response += token + " "
            response_placeholder.markdown(full_response)
            time.sleep(0.05)  # typing delay
        return full_response

    # Otherwise stream from LLM
    for chunk in model.stream(messages):
        # Anthropic returns tokens in chunk.content
        if hasattr(chunk, "content") and chunk.content:
            token = chunk.content
        elif hasattr(chunk, "delta") and chunk.delta:  # fallback
            token = chunk.delta
        else:
            token = ""

        full_response += token
        response_placeholder.markdown(full_response)

    return full_response


