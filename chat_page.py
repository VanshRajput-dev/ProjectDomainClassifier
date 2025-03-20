import streamlit as st
import requests
import time

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000"

# Ensure investor name is stored
if "investor_name" not in st.session_state:
    st.session_state["investor_name"] = "Unknown Investor"  # Default value

if "username" not in st.session_state:
    st.session_state["username"] = "Fundraiser"  # Default user

# Chat variables
investor_name = st.session_state["investor_name"]
username = st.session_state["username"]

st.title(f"Chat with {investor_name}")

# Function to fetch chat history
def fetch_chat():
    response = requests.get(f"{BACKEND_URL}/chat/{username}/{investor_name}")
    if response.status_code == 200:
        return response.json()["chat_history"]
    return []

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = fetch_chat()

# Display chat messages
chat_box = st.empty()
messages = [f"{msg['sender']}:** {msg['message']}" for msg in st.session_state["chat_history"]]
chat_box.markdown("\n".join(messages))

# Message input
message_input = st.text_input("Type a message...")

if st.button("Send"):
    if message_input.strip():
        # Send message to backend
        response = requests.post(f"{BACKEND_URL}/chat/", json={
            "sender": username,
            "receiver": investor_name,
            "message": message_input.strip()
        })
        
        if response.status_code == 200:
            st.session_state["chat_history"].append({"sender": username, "message": message_input.strip()})
            messages.append(f"*You:* {message_input.strip()}")
            chat_box.markdown("\n".join(messages))
        else:
            st.error("Failed to send message. Try again!")

# Auto-refresh chat every 5 seconds
while True:
    time.sleep(5)
    new_chat = fetch_chat()
    if new_chat != st.session_state["chat_history"]:
        st.session_state["chat_history"] = new_chat
        messages = [f"{msg['sender']}:** {msg['message']}" for msg in new_chat]
        chat_box.markdown("\n".join(messages))