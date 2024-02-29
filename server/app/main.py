from fastapi import FastAPI, HTTPException
import json
import os
from openai import OpenAI
import yfinance as yf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import datetime
import uvicorn


app = FastAPI()

# Load OpenAI API key
config_file_path = '/etc/python-gpt.json'
openai_api_key = None

if os.path.exists(config_file_path):
    with open(config_file_path) as config_file:
        openai_api_key = json.load(config_file).get('OPENAI_API_KEY', "")
else:
    raise FileNotFoundError(f"Config file not found at {config_file_path}")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Hello World route
@app.get("/api/hello")
def hello():
    msg={"message": "Hello, World!", "version": "0.0.5"}
    print(msg)
    return msg

# API route for chat
@app.post("/api/chat")
def chat(data: dict):
    message = data.get("message")
    if message:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return {"message": response.choices[0].message.content}
    else:
        raise HTTPException(status_code=400, detail="Invalid request")

# API route for stock data
@app.get("/api/stock/{ticker}")
def get_stock_data(ticker: str):
    try:
        stock_data = yf.download(ticker, period="1y")
        ticker_data = yf.Ticker(ticker)
        close_prices = np.array(stock_data['Close']).reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        close_prices_scaled = scaler.fit_transform(close_prices)

        X, y = [], []
        look_back = 90
        for i in range(look_back, len(close_prices_scaled)):
            X.append(close_prices_scaled[i-look_back:i, 0])
            y.append(close_prices_scaled[i, 0])
        X, y = np.array(X), np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
            LSTM(units=50),
            Dense(units=1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)

        predicted_prices_scaled = []
        last_days = close_prices_scaled[-look_back:]
        for _ in range(30):
            prediction = model.predict(np.array([last_days]))
            predicted_prices_scaled.append(prediction[0, 0])
            last_days = np.roll(last_days, shift=-1)
            last_days[-1] = prediction

        predicted_prices = scaler.inverse_transform(np.array(predicted_prices_scaled).reshape(-1, 1))
        predicted_prices = [price for sublist in predicted_prices.tolist() for price in sublist]

        # Get the current date
        current_date = datetime.date.today()
        # Generate future dates starting from the current date
        dates = [current_date + datetime.timedelta(days=i) for i in range(len(predicted_prices))]
        # Create list of dictionaries containing date, price, and id
        price_objects = [{"id": i+1, "date": str(date), "price": price} for i, (date, price) in enumerate(zip(dates, predicted_prices))]
        
        # Pretty print ticker_data.info
        ticker_info_dict = ticker_data.info
        ticker_info_str = json.dumps(ticker_info_dict, indent=4)
        print(ticker_info_str)

        payload={"ticker": ticker, "ticker_info": ticker_info_dict, "predicted_prices": price_objects}

        return payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run("main_v3:app", host="0.0.0.0", port=6969,)

