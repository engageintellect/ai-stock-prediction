import requests
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error


days_to_predict = 30
stock_ticker='spy'

# Fetch data from the API endpoint
url = f'http://localhost:8000/stock/{stock_ticker}'
response = requests.get(url)
data = response.json()
print(data)

# Extract 'Close' prices from the JSON data
close_prices = np.array([item['Close'] for item in data]).reshape(-1, 1)

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

# Make predictions for the next 10 days
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
