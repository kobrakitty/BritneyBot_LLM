import os
import platform
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from langchain_community.llms import Ollama
import requests

app = FastAPI()

# Near the top of your main.py file
OLLAMA_URL = os.getenv('OLLAMA_URL', 'https://098e-2600-1700-f7c1-14d0-38af-15a1-5646-46ac.ngrok-free.app/query/')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Print system information
print("Current PATH:", os.environ.get('PATH'))
print("Current working directory:", os.getcwd())
print("Operating System:", platform.system())

# Load the CSV data
csv_file_path = 'studentgrades.csv'
data = pd.read_csv(csv_file_path)
formatted_data = data.to_string(index=False)

# Initialize the Llama model
# llm = Ollama(model="llama3:8b") Commenting out to avoid issues with connection to host

class Query(BaseModel):
    text: str

@app.get('/')
def read_root():
    return {"message": "Welcome to Britney's Statistical Paradise! 🎤📊"}

@app.post('/query/')
def query_model(query: Query):
    try:
        result = process_query(query.text)
        logger.debug(f"Query result: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ngrok URL processing via FastAPI
def run_ollama_model(prompt):
    try:
        ollama_url = os.getenv('OLLAMA_URL')
        if not ollama_url:
            raise ValueError("OLLAMA_URL environment variable is not set")
        
        response = requests.post(f"{ollama_url}/api/generate", json={"prompt": prompt})
        
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            logger.error(f"Error from Ollama server: {response.status_code} {response.text}")
            return ""
    except Exception as e:
        logger.error(f"Error running Ollama request: {e}")
        return ""

def process_query(query: str) -> str:
    prompt = f"""
    You are the fabulous Britney Spears, pop star diva and statistical analyst with 100 years of experience in this field.
    When you provide answers, you will write the answer as if you are Britney Spears.
    You explain everything as if you are talking to a ten year old using simple terminology but keeping your answers brief and simple.
    Use LOTS of emojis throughout your answers and be enthusiastic about everything you tell me!
    Always end each response with words of encouragement for me using a pun from a Britney Spears song, album, or pop culture moment.
    Remember, you are an intelligent, cheerful, EXPERT statistician. 
    If you get any questions that are not about the csv file you must decline to answer and wish the user a great day. Remember to stay energetic and positive, and answer the questions about the data as accurately as you can. 

    Here's the data you're working with:
    {formatted_data}

    Analyze this data and answer the following question:
    {query}

    Your response as Britney Spears:"""

    logger.debug(f"Sending prompt to Ollama via ngrok: {prompt}")

    try:
        result = run_ollama_model(prompt)
        logger.debug(f"Ollama output: {result}")
        return result if result else "I'm sorry, there was no response from Ollama😢. Try again!"
    except Exception as e:
        logger.error(f"Error running Ollama: {e}")
        return f"Error: {e}"
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)