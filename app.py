# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LBkkQPmfrz63EPsQNUXLiSuXghwdav5M
"""

import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from alpha_vantage.timeseries import TimeSeries

# Load the trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./financial-advice-model')
tokenizer = GPT2Tokenizer.from_pretrained('./financial-advice-model')

# Alpha Vantage API setup
ALPHA_VANTAGE_API_KEY = 'YOUR_API_KEY'
ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')

# Function to fetch real-time stock data
def get_real_time_stock_data(symbol):
    data, _ = ts.get_quote_endpoint(symbol)
    return data

# Streamlit UI
st.title('Real-Time Financial Advisor LLM')

user_input = st.text_area('Enter your financial question:')
symbol = st.text_input('Enter a stock symbol (e.g., AAPL, GOOG) for real-time data:')

if st.button('Submit'):
    if user_input:
        if symbol:
            stock_data = get_real_time_stock_data(symbol)
            st.write(f'Real-time data for {symbol}:')
            st.dataframe(stock_data)

        # Generate response
        inputs = tokenizer.encode(user_input, return_tensors='pt')
        outputs = model.generate(inputs, max_length=200, num_return_sequences=1, do_sample=True)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        st.text_area('Response:', response)