from fastapi import FastAPI
from typing import Dict
import json
from openai import OpenAI
import os

app = FastAPI()

# Load your OpenAI API key from a config file
config_file_path = '/etc/python-gpt.json'
if os.path.exists(config_file_path):
    with open(config_file_path) as config_file:
        config = json.load(config_file)
        if 'OPENAI_API_KEY' in config:
            openai_api_key = config['OPENAI_API_KEY']
        else:
            raise ValueError("OPENAI_API_KEY not found in config file")
else:
    raise FileNotFoundError(f"Config file not found at {config_file_path}")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

import yfinance as yf

@app.get("/stock/{ticker}")
def get_stock_data(ticker: str):
    try:
        # Get data for the past year
        stock_data = yf.download(ticker, period="120d")

        # Convert the data to dictionary format
        stock_data_dict = stock_data.reset_index().to_dict(orient='records')

        return stock_data_dict
    except Exception as e:
        return {"error": str(e)}

@app.post("/chat")
def chat(data: Dict[str, str]):
    message = data.get("message")
    if message:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ])
        return {"message": response.choices[0].message.content}
    else:
        return {"message": "Invalid request"}

