import streamlit as st
from langchain.llms import Ollama

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

# Function for string dialogue
def get_string_dialogue(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    return f"{string_dialogue} {prompt_input} Assistant: "

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = st.write_stream(ollama.stream(get_string_dialogue(prompt)))
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
