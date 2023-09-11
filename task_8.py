import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta
import requests
import streamlit as st
import time

# Load BTC, ETH, LTC data
btc_data = pd.read_csv('btc_data.csv')
eth_data = pd.read_csv('etc_data.csv')
ltc_data = pd.read_csv('ltc_data.csv')

def predict_price(data, specific_date):
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data = data.resample('D').mean().ffill()
    train_data = data[data.index < specific_date]

    p, d, q = 1, 1, 1  # ARIMA parameters
    P, D, Q, s = 1, 1, 1, 7  # Seasonal parameters (daily data with weekly seasonality)

    model = SARIMAX(train_data['close'], order=(p, d, q), seasonal_order=(P, D, Q, s))
    results = model.fit()

    specific_date_dt = datetime.strptime(specific_date, "%Y-%m-%d")
    predicted_price = results.get_forecast(steps=1).predicted_mean.iloc[0]

    return predicted_price, specific_date_dt

def fetch_data(pair, limit):
    params = {
        "fsym": pair.split("/")[0],
        "tsym": pair.split("/")[1],
        "limit": limit,
        "aggregate": 1
    }

    response = requests.get(HISTO_DAY_URL, params=params)
    data = response.json()
    
    df = pd.DataFrame(data['Data'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    df['close'] = df['close'].astype(float)
    
    return df

def calculate_moving_averages(df, short_window, long_window):
    df['SMA50'] = df['close'].rolling(window=short_window).mean()
    df['SMA200'] = df['close'].rolling(window=long_window).mean()
    return df

def execute_order(order_type, price, quantity):
    global account_balance
    
    if order_type == 'buy':
        st.write(f"Executing BUY order at price {price}, quantity {quantity}")
        account_balance -= price * quantity
        st.write(f"Updated account balance: {account_balance} USDT")
    
    elif order_type == 'sell':
        st.write(f"Executing SELL order at price {price}, quantity {quantity}")
        account_balance += price * quantity
        st.write(f"Updated account balance: {account_balance} USDT")

# CryptoCompare API endpoints
BASE_URL = "https://min-api.cryptocompare.com/data/"
HISTO_DAY_URL = BASE_URL + "histoday"
PAIR = "BTC/USDT"  # Trading pair
LIMIT = 200  # Number of data points to retrieve

# Define strategy parameters
short_window = 50
long_window = 200

# Initial account balance (for demonstration)
account_balance = 10000  # USDT

# Streamlit setup
st.title("Crypto Trading Bot Simulation")
st.sidebar.title("Bot Settings")

# User-defined settings
bot_speed = st.sidebar.slider("Bot Speed (seconds)", 1, 60, 10)
initial_balance = st.sidebar.number_input("Initial Account Balance (USDT)", min_value=1, value=10000)
pair = st.sidebar.text_input("Trading Pair (e.g., BTC/USDT)", value="BTC/USDT")
short_window = st.sidebar.number_input("Short Window (days)", min_value=1, value=50)
long_window = st.sidebar.number_input("Long Window (days)", min_value=1, value=200)

# Display user-defined settings
st.sidebar.subheader("Bot Configuration")
st.sidebar.write(f"Initial Balance: {initial_balance} USDT")
st.sidebar.write(f"Trading Pair: {pair}")
st.sidebar.write(f"Short Window: {short_window} days")
st.sidebar.write(f"Long Window: {long_window} days")

col1, col2 = st.columns(2)
start_bot = col1.button("Start Bot")
stop_bot = col2.button("Stop Bot")

def main():
    while start_bot:
        # Fetch and preprocess data
        data = fetch_data(pair, LIMIT)
        data = calculate_moving_averages(data, short_window, long_window)

        st.write(f"Data fetched at {data.index[-1]}")
        st.write(f"SMA50: {data['SMA50'].iloc[-1]}, SMA200: {data['SMA200'].iloc[-1]}")

        # Implement a simple crossover strategy
        if data['SMA50'].iloc[-2] < data['SMA200'].iloc[-2] and data['SMA50'].iloc[-1] >= data['SMA200'].iloc[-1]:
            st.write(f"Buy signal at {data.index[-1]}")
            # Hypothetical buy order
            execute_order('buy', data['close'].iloc[-1], 1)
        
        elif data['SMA50'].iloc[-2] > data['SMA200'].iloc[-2] and data['SMA50'].iloc[-1] <= data['SMA200'].iloc[-1]:
            st.write(f"Sell signal at {data.index[-1]}")
            # Hypothetical sell order
            execute_order('sell', data['close'].iloc[-1], 1)
        
        else:
            st.write("Hold")  # Neither buy nor sell conditions met
        
        time.sleep(bot_speed)  # Sleep for user-defined seconds

    # ... (previous code)

# Streamlit setup
st.title("Crypto Trading Bot with Prediction")
st.sidebar.title("Bot Settings")

# User-defined settings
specific_date = st.sidebar.date_input("Enter a Date")
specific_date = specific_date.strftime("%Y-%m-%d")  # Convert to string

# Display user-defined settings
st.sidebar.subheader("Bot Configuration")
st.sidebar.write(f"Specific Date: {specific_date}")

# Add a button to trigger predictions
predict_button = st.sidebar.button("Predict Prices")


if predict_button:
    # Predict prices for Bitcoin, Litecoin, and Ethereum
    btc_predicted_price, btc_specific_date = predict_price(btc_data, specific_date)
    eth_predicted_price, eth_specific_date = predict_price(eth_data, specific_date)
    ltc_predicted_price, ltc_specific_date = predict_price(ltc_data, specific_date)

    # Display predictions
    st.write(f"The BTC price on {btc_specific_date} was predicted to be ${btc_predicted_price:.2f}")
    st.write(f"The ETH price on {eth_specific_date} was predicted to be ${eth_predicted_price:.2f}")
    st.write(f"The LTC price on {ltc_specific_date} was predicted to be ${ltc_predicted_price:.2f}")




if __name__ == '__main__':
    main()
    if stop_bot:  # Stop the bot when the "Stop Bot" button is pressed
        output_area.text("Bot stopped.")
