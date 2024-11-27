from openai import OpenAI
import streamlit as st
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
secret_key = os.environ.get("SECRET_KEY")

with st.sidebar:
    secret_input = st.text_input("Secret Key", type="password")

st.title("Chat with ECC")
st.caption("Essential Cybersecurity Controls (ECC-1:2018)")

ecc = open('ecc-en.txt', 'r').read()

if not openai_api_key:
    st.info("Please add OpenAI API key to continue.")
    st.stop()

if not secret_key:
    st.info("Please add Secret Key to continue.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state["messages"] = [ 
        {
            'role': 'system',
            'content': f"""
# Instructions:
- You are ECC Bot and do not belong to any entity or organization.
- With no previous knowledge, your only task is to answer the question based on the context. 
- Refrain from criticizing the context. 
- Do not use bad words.
- Answer in English.
- Do not compare the context against any other policies, standards, or frameworks.

# Context:
{ecc}
"""
        }
    ]

for msg in st.session_state.messages:
    if msg['role'] == 'system': continue

    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not secret_input:
        st.error("Please enter the secret key to continue.")
        st.stop()

    if secret_input != secret_key:
        st.error("Invalid secret key.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.chat_message('assistant'):
        response = st.write_stream(client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages, stream=True))
        msg = response
        st.session_state.messages.append({"role": "assistant", "content": msg})