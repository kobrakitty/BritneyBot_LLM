import os
import platform
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import requests

app = FastAPI()

# Load the CSV data
csv_file_path = 'studentgrades.csv'
try:
    data = pd.read_csv(csv_file_path)
    formatted_data = data.to_string(index=False)
except FileNotFoundError:
    print(f"Error: CSV file '{csv_file_path}' not found.")
    formatted_data = "No data available"
except pd.errors.EmptyDataError:
    print(f"Error: CSV file '{csv_file_path}' is empty.")
    formatted_data = "No data available"
except pd.errors.ParserError:
    print(f"Error: Unable to parse CSV file '{csv_file_path}'.")
    formatted_data = "No data available"

class Query(BaseModel):
    text: str

# This is the fastAPI welcome page placeholder
@app.get('/')
def read_root():
    return {"message": "Welcome to Britney's Statistical Paradise! 🎤📊"}

#This defines the query for fastAPI
@app.post('/query/')
def query_model(query: Query):
    try:
        result = process_query(query.text)
        logger.debug(f"Query result: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
       
# This is the ngrok URL API handing via FastAPI
def run_ollama_model(prompt):
    """Run the Ollama model on the given prompt."""
    try:
        # For DEPLOYMENT, uncomment this line for the ngrok URL - always change this when ngrok restarts with free version:
        OLLAMA_URL = 'https://762c-2600-1700-f7c1-14d0-cc3c-744c-483a-ce1a.ngrok-free.app'
        
        # For TESTING locally, uncomment this line:
        # OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        
        #Request from ngrok to Ollama local server
        response = requests.post(OLLAMA_URL, json={"text": prompt}, timeout=30)
        
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        return response.json().get("result", "")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Ollama server: {e}")
        return "Oops! I couldn't reach my brain right now. Try again later, baby! 🎵"
    except ValueError as e:
        logger.error(f"Error parsing JSON response: {e}")
        return "Oops! I got confused with the response. Can you ask me again, sweetie? 🎤"
    except Exception as e:
        logger.error(f"Unexpected error running Ollama model: {e}")
        return "Something unexpected happened. Let's give it another shot! 💃"

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Print system information
print("Current PATH:", os.environ.get('PATH'))
print("Current working directory:", os.getcwd())
print("Operating System:", platform.system())

def process_query(query: str) -> str:
    if not query.strip():
        return "Oops! You didn't ask me anything, honey! Give me a real question to work with! 🎶"
    
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
    
    return run_ollama_model(prompt)
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)