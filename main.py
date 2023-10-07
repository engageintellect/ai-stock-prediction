from fastapi import FastAPI
from typing import Dict
import json
import openai
from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

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


# Load your OpenAI API key from a config file
with open ('/etc/python-gpt.json') as config_file:
   config = json.load(config_file)


# Set your OpenAI API key
openai.api_key = config['OPENAI_API_KEY']

@app.post("/chat")
def chat(data: Dict[str, str]):
    message = data.get("message")
    if message:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return {"message": response.choices[0].message["content"]}
    else:
        return {"message": "Invalid request"}

