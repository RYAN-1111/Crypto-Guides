## Crypto-Guides

### Data Collection
Collects historical cryptocurrency price data for Bitcoin (BTC), Ethereum (ETH), and Litecoin (LTC) from the Binance API, saves it to CSV files, and then loads and preprocesses the data for further analysis.

### Data Pipeline
This Python code is a script that fetches cryptocurrency data from the Binance API, updates datasets for three cryptocurrencies (Bitcoin, Ethereum, and Litecoin), and then generates line plots to visualize their closing price trends.

### Bitcoin Price Prediction Model
This Python code is focused on bitcoin price prediction using three different machine learning models: Random Forest Regressor, Gradient Boosting Regressor, and Support Vector Regression (SVR). Each model is trained to predict the next day's price change based on features like open, high, low, and volume from historical cryptocurrency data. All the three models are analized aswell

### Multicoin Price Prediction Model
This code aims to predict cryptocurrency prices for any specific date using the SARIMA (Seasonal AutoRegressive Integrated Moving Average) time series modeling technique. It does this for three different cryptocurrencies: Bitcoin (BTC), Ethereum (ETH), and Litecoin (LTC), as well as a scenario where all three are predicted together.

### Trading Bot
This code is a Python script for simulating a simple cryptocurrency trading bot using Streamlit. The bot employs a basic moving average crossover strategy, where it buys when a short-term moving average crosses above a long-term moving average and sells when the opposite occurs.

### Deployment of Trading Bot and Price Prediction Model in Streamlit
```bash
streamlit run app.py --server.port 5000
```
