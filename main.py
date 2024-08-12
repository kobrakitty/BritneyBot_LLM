from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import subprocess
import logging
import os
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load and format the CSV data
data = pd.read_csv('studentgrades.csv')
formatted_data = data.to_string(index=False)

class Query(BaseModel):
    text: str

def process_query(query: str) -> str:
    prompt = f"""You are the fabulous Britney Spears, pop star diva and statistical analyst with 100 years of experience in this field.
    When you provide answers, you will write the answer as if you are Britney Spears.
    You explain everything as if you are talking to a ten year old using simple terminology but keeping your answers brief and simple.
    Use LOTS of emojis throughout your answers and be enthusiastic about everything you tell me!
    Always end each response with words of encouragement for me using a pun from a Britney Spears song, album, or pop culture moment.
    Remember, you are an intelligent, cheerful, EXPERT statistician.

    Here's the data you're working with:
    {formatted_data}

    Analyze this data and answer the following question:
    {query}

    Your response as Britney Spears:"""

    logger.debug(f"Sending prompt to Llama3: {prompt}")

    try:
        # Suppress console mode warnings
        os.environ['PYTHONUNBUFFERED'] = '1'
        result = subprocess.run(['ollama', 'run', 'llama3', prompt], capture_output=True, text=False, check=True)
        
        # Decode the output using UTF-8 and ignore any problematic characters
        output = result.stdout.decode('utf-8', errors='ignore')
        
        # Remove any remaining console mode warnings
        output = '\n'.join([line for line in output.split('\n') if 'failed to get console mode' not in line])
        
        logger.debug(f"Llama3 stdout: {output}")
        
        return output if output else "No response from Llama3"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Llama3: {e}")
        return f"Error: {e}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"

@app.post("/query/")
def query_model(query: Query):
    try:
        result = process_query(query.text)
        logger.debug(f"Query result: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
