import streamlit as st
import ollama 
from typing import Dict, Generator

def ollama_generator(model_name: str, messages: Dict) -> Generator:
    stream = ollama.chat(
        model=model_name, messages=messages, stream=True)
    for chunk in stream:
        yield chunk['message']['content']

st.title("John Lee Ka-chiu")

st.image("./assets/avatar.jpg", width=480)

st.text("Type something to start a conversation with the chief.")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.selected_model = "lee:latest"

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar = "./assets/icon.png"):
        st.markdown(message["content"])

if prompt := st.chat_input("How could I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar = "./assets/icon.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar = "./assets/icon.png"):
        response = st.write_stream(ollama_generator(
            st.session_state.selected_model, st.session_state.messages))

    st.session_state.messages.append(
        {"role": "assistant", "content": response})