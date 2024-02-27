from fastapi import FastAPI
from typing import Dict
import json
from openai import OpenAI
import os
import yfinance as yf
import requests
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error

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

# Helloworld route
@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

# Initialize API route for chat
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

# Initialize API route for stock data
@app.get("/stock/{ticker}")
def get_stock_data(ticker: str):
    try:
        # Get data for the past year
        stock_data = yf.download(ticker, period="120d")

        # Convert the data to dictionary format
        stock_data_dict = stock_data.reset_index().to_dict(orient='records')

        # Choose how many days to predict
        days_to_predict = 30

        # Extract 'Close' prices from the JSON data
        close_prices = np.array([item['Close'] for item in stock_data_dict]).reshape(-1, 1)

        # Normalize the data using MinMaxScaler
        scaler = MinMaxScaler(feature_range=(0, 1))
        close_prices_scaled = scaler.fit_transform(close_prices)

        # Prepare the data for LSTM model (input features and target variable)
        X, y = [], []
        look_back = 90  # Number of previous days' close prices to use for prediction
        for i in range(look_back, len(close_prices_scaled)):
            X.append(close_prices_scaled[i-look_back:i, 0])
            y.append(close_prices_scaled[i, 0])
        X, y = np.array(X), np.array(y)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Reshape input data for LSTM (samples, time steps, features)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        # Build the LSTM model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        model.fit(X_train, y_train, epochs=20, batch_size=32)

        # Make predictions
        predicted_prices = model.predict(X_test)
        predicted_prices = scaler.inverse_transform(predicted_prices)  # Reverse scaling for predictions

        # Evaluate the model (you can use various metrics here)
        loss = model.evaluate(X_test, y_test)

        # Print the loss (mean squared error)
        print('Mean Squared Error on Test Data:', loss)

        # Calculate Mean Squared Error (MSE)
        mse = mean_squared_error(y_test, predicted_prices)
        print('Mean Squared Error on Test Data:', mse)

        # Calculate Root Mean Squared Error (RMSE)
        rmse = np.sqrt(mse)
        print('Root Mean Squared Error on Test Data:', rmse)

        # Reshape the last 'look_back' days of data to predict the next 'days_to_predict' days
        last_days = close_prices_scaled[-look_back:]
        X_pred = []
        X_pred.append(last_days)
        X_pred = np.array(X_pred)

        # Make predictions for the next X days
        predicted_prices_scaled = []
        for _ in range(days_to_predict):
            prediction = model.predict(X_pred)  # Predict the next day
            predicted_prices_scaled.append(prediction[0, 0])

            # Update X_pred for the next prediction
            last_days = np.roll(last_days, shift=-1)  # Shift elements to the left
            last_days[-1] = prediction  # Replace the last element with the new prediction
            X_pred = np.array([last_days])  # Reshape for the next prediction

        # Inverse transform the predicted prices to get the actual prices
        predicted_prices = scaler.inverse_transform(np.array(predicted_prices_scaled).reshape(-1, 1))

        # Print the predicted prices for the next 10 days
        print(f"\nPredicted Prices for the Next {days_to_predict} Days:")
        print(predicted_prices)
        payload = {"stock_data": stock_data_dict,"predicted_prices": predicted_prices.tolist()}
        predictions = {f"{days_to_predict} day predicted prices.": predicted_prices.tolist()}

        # Return the stock data and predicted prices
        return predictions

    except Exception as e:
        return {"error": str(e)}

