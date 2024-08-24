# This is the streamlit frontend UI/UX setup
import streamlit as st
import pandas as pd
import requests
import os

API_URL = os.getenv('API_URL', 'https://britneybot-llm.onrender.com')

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
        with st.spinner("Britney is thinking... 💭"):
            response = requests.post(f"{API_URL}/query/", json={"text": user_question}, timeout=30)
        
        if response.status_code == 200:
            result = response.json()["result"]
            if result and len(result) > 20:  # Ensure we have a substantial response
                st.write(result)
            else:
                st.warning("Oops! Britney's response was too short. Can you try asking again? 🎤💖")
        else:
            st.error(f"An error occurred while processing your request. Status code: {response.status_code}")
    except requests.RequestException as e:
        st.error(f"Unable to reach the API. Error: {e}")
        
# Display the data
st.subheader("Student Grades Data📑 ")
st.dataframe(data)

#Footer styling
st.write("I am AI bot built by built by Glitter Pile AI using open source Ollama model llama3:8b. I have been trained to answer questions about this sample data set in a fun and emoji-filled way! Hope you enjoyed your chat with me! xo💋BritneyBot")
st.write("*Visit www.glitterpile.blog for more fun things!*")