import streamlit as st
from langchain.llms import Ollama
import time

# App title
st.set_page_config(page_title="👨🏻‍💻 API Security Chatbot")
with st.sidebar:
    st.title("👨🏻‍💻 API Security Chatbot")

# Initialize Ollama
ollama = Ollama(model="api-secexpert")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating Ollama response
def generate_ollama_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    response = ollama.__call__(prompt=f"{string_dialogue} {prompt_input} Assistant: ")
    return response

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = generate_ollama_response(prompt)
        placeholder = st.empty()
        full_response = ''
        for char in response:  # Assume response is a string
            full_response += char
            placeholder.markdown(full_response)
            time.sleep(0.05)  # Adjust the delay as needed
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
