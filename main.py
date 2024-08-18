import os
import platform
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import requests

app = FastAPI()

# For TESTING locally, uncomment this line:
# OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')

# For DEPLOYMENT, uncomment this line:
OLLAMA_URL = os.getenv('OLLAMA_URL', 'https://22c9-2600-1700-f7c1-14d0-cc3c-744c-483a-ce1a.ngrok-free.app')

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
    """Run the Ollama model on the given prompt."""
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json={"prompt": prompt, "model": "llama3:8b"})
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json().get('response', '')
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Ollama: {e}")
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
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return ""
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)