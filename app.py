# This is the streamlit frontend UI/UX setup
import streamlit as st
import pandas as pd
import requests
import os

API_URL = os.getenv('API_URL', "https://britneybot-llm.onrender.com")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("studentgrades.csv")

data = load_data()

st.title("BritneyBot: Pop Star Statistician 💃🎤✨📊✨📈✨")
st.write("Ask me about the student grades data below, and I'll answer as Britney!")

# Add some Britney-themed decorations
st.sidebar.title("Hi, Cuties! It's me, BritneyBot💋")
st.sidebar.image("britneybot2.jpg", use_column_width=True)
st.sidebar.write("I'm so glad you're here! Even though I love studying, I also love making pop music! What are my top favorite songs, EVER?? I'm so glad you asked!:")
st.sidebar.write("💖 ...Baby One More Time 💖")
st.sidebar.write("👗 Oops!... I Did It Again 👗")
st.sidebar.write("🐍 Toxic 🐍")
st.sidebar.write("🥀 Gimme More 🥀")

# User input
user_question = st.text_input("Okay let's do this! What's your question about the student grades data?🤔")

if user_question:
    try:
        # Send request to FastAPI backend
        response = requests.post(f"{API_URL}/query/", json={"text": user_question})
        
        if response.status_code == 200:
            # Display the response
            st.write(response.json()["result"])
        else:
            st.error(f"An error occurred while processing your request. Status code: {response.status_code}")
    except requests.RequestException as e:
        st.error(f"Unable to reach the API. Error: {e}")

# Display the data
st.subheader("Student Grades Data📑 ")
st.dataframe(data)

#Footer styling
st.write("I am AI bot built by built by Glitter Pile AI using Ollama model llama3. I have been trained to answer questions about this sample data set in a fun and emoji-filled way! Hope you enjoyed your chat with me! xo💋BritneyBot")
st.write("*Visit www.glitterpile.blog for more fun things!*")
