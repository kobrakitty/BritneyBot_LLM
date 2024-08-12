# This is the streamlit frontend UI/UX setup

import streamlit as st
import pandas as pd
import requests
import os

API_URL = os.getenv('API_URL', 'https://britney-the-statistician.onrender.com')

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("studentgrades.csv")

data = load_data()

st.title("Britney Spears: Pop Star Statistician 🎤📊")
st.write("Ask me about the student grades data below, and I'll answer as Britney!")

# Add some Britney-themed decorations
st.sidebar.image("britneybot2.jpg", use_column_width=True)
st.sidebar.write("Besides LOVING math and statistics, my other fave thing is makin' music! What are my top favorite songs, EVER?? I'm so glad you asked! My fave songs...!:")
st.sidebar.write("💖 ...Baby One More Time 💖")
st.sidebar.write("🎵 Oops!... I Did It Again 🎵")
st.sidebar.write("💃 Toxic 💃")
st.sidebar.write("🌟 Gimme More 🌟")

# User input
user_question = st.text_input("What's your question about the data?")

if user_question:
    # Send request to FastAPI backend
    response = requests.post(f"{API_URL}/query/", json={"text": user_question})
    
    if response.status_code == 200:
        # Display the response
        st.write(response.json()["result"])
    else:
        st.error("An error occurred while processing your request.")

# Display the data
st.subheader("Student Grades Data")
st.dataframe(data)

st.write("I'm an AI bot built by built by Glitter Pile AI. I have been trained as a statistician that can answer questions about this data in a fun and emoji-filled way! Hope you enjoyed your chat with me! xo, BritneyBot")
