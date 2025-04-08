import streamlit as st
import openai
import os
from dotenv import load_dotenv

import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🧗‍♀️ Mountaineering Chatbot")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful mountaineering chatbot."}
    ]

# Show chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask about climbing, gear, training, etc...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)

    # Add to message history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API with full history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Show assistant response
    st.chat_message("assistant").markdown(reply)

    # Add assistant reply to history
    st.session_state.messages.append({"role": "assistant", "content": reply})

