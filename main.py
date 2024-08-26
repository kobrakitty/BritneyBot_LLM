import os
import platform
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from huggingface_hub import InferenceClient

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
HF_API_TOKEN = os.getenv('HF_API_TOKEN')

# Model name (public model)
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"

# API Error handling
if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN must be set in environment variables")

# Initialize InferenceClient
client = InferenceClient(MODEL_NAME, token=HF_API_TOKEN)

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

@app.get('/')
def read_root():
    return {"message": "Welcome to Britney's Statistical Paradise! 🎤📊"}

@app.post('/query/')
async def query_model(query: Query):
    try:
        result = await process_query(query.text)
        logger.debug(f"Query result: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_huggingface_model(prompt):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = ""
        for message in client.chat_completion(
            messages=messages,
            max_tokens=300,
            temperature=0.6,
            top_p=0.90,
            stream=True
        ):
            response += message.choices[0].delta.content or ""
        
        logger.debug(f"API Response: {response}")
        
        return response.strip()
    except Exception as e:
        logger.error(f"Error communicating with Hugging Face API: {e}")
        return f"Error: {str(e)}. Please check your API token and permissions."

async def process_query(query: str) -> str:
    if not query.strip():
        return "Oops! You didn't ask me anything, honey! Give me a new question to work with, please!"
    
    prompt = f"""You are the fabulous Britney Spears, pop star diva and statistical analyst with 100 years of experience in this field. When you provide answers, you will write the answer as if you are Britney Spears but keep it brief and to the point. While keeping it relatively brief, you will explain the math as if you are talking to a ten year old using simple terminology. So keep your answer simple. Use a lot of fun emojis throughout your answers and be enthusiastic about everything you write. Always end each response with words of encouragement for me using a pun from a Britney Spears song, album, or pop culture moment. Remember, you are an intelligent, cheerful, EXPERT statistician who explains info in a succinct but joyful way. If you get any questions that are not about the csv file, decline to answer and remind them that you can only answer questions about the Student Grades data set. Stay energetic and positive, and answer questions as accurately as you can. 

    Here's the data you're working with:
    {formatted_data}

    Analyze this data and answer the following question:
    {query}"""
    
    return await run_huggingface_model(prompt)

if __name__ == "__main__":
    print("Current PATH:", os.environ.get('PATH'))
    print("Current working directory:", os.getcwd())
    print("Operating System:", platform.system())
    
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)