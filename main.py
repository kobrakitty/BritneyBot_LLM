import os
import platform
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import requests
from huggingface_hub import HfApi

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

# Hugging Face API setup
hf_api = HfApi()
HF_API_TOKEN = os.getenv('HF_API_TOKEN')
HF_INFERENCE_ENDPOINT = os.getenv('HF_INFERENCE_ENDPOINT')

if not HF_API_TOKEN or not HF_INFERENCE_ENDPOINT:
    raise ValueError("HF_API_TOKEN and HF_INFERENCE_ENDPOINT must be set in environment variables")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

def run_huggingface_model(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}"
        }
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.95,
                "do_sample": True
            }
        }
        response = requests.post(HF_INFERENCE_ENDPOINT, headers=headers, json=payload, timeout=30)
        
        response.raise_for_status()
        full_response = response.json()[0]['generated_text']
        
        # Extract only Britney's response
        britney_response = full_response.split("Your response as Britney Spears:")[-1].strip()
        
        # Remove any remaining prompt text or data
        unwanted_texts = [
            "Here's the data you're working with:",
            "Analyze this data and answer the following question:",
            "Student Math_Grade Physics_Grade"
        ]
        for text in unwanted_texts:
            if text in britney_response:
                britney_response = britney_response.split(text)[0].strip()
        
        # Ensure the response doesn't end abruptly
        sentences = britney_response.split('.')
        if len(sentences) > 1:
            britney_response = '. '.join(sentences[:-1]) + '.'
        
        return britney_response.strip()
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Hugging Face API: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

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
    
    return run_huggingface_model(prompt)

if __name__ == "__main__":
    print("Current PATH:", os.environ.get('PATH'))
    print("Current working directory:", os.getcwd())
    print("Operating System:", platform.system())
    
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)