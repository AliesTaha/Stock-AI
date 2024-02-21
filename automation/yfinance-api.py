import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import argparse
import os

# useful fiannce indicators

import pandas as pd
import yfinance as yf

def calculate_atr(ticker_symbol, start_date=datetime().today - 14, end_date=datetime().today, n=14):
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    data['High-Low'] = data['High'] - data['Low']
    data['High-PrevClose'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-PrevClose'] = abs(data['Low'] - data['Close'].shift(1))
    data['TR'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
    data['ATR'] = data['TR'].rolling(window=n, min_periods=1).mean()
    
    return data[['Close', 'ATR']]



def calculate_momentum(ticker_symbol, start_date=datetime().today - 14, end_date=datetime().today, n=14): # short term momentum
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    data['Momentum'] = data['Close'] - data['Close'].shift(n)
    return data[['Close', 'Momentum']]


def calculate_macd(ticker_symbol, start_date=datetime().today - 365, end_date=datetime().today):
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal_line = macd.ewm(span=9, adjust=False).mean()
    data['MACD'] = macd
    data['Signal Line'] = signal_line
    return data[['Close', 'MACD', 'Signal Line']]


def fetch_and_save_ticker_data(ticker_symbol, output_directory):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    output_file_path = os.path.join(output_directory, f"{ticker_symbol}_last_30_days_data.csv")
    with open(output_file_path, 'w') as file:
        file.write(data.to_csv())

    print(f"Data for {ticker_symbol} written to {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Download and save the last 30 days of stock data for each ticker symbol listed in the input file.")
    parser.add_argument("file_to_ticker_list", type=str, help="Path to the file containing a list of ticker symbols, one per line")
    parser.add_argument("--output_directory", type=str, default=".", help="Directory to save the output files (default is current directory)")
    args = parser.parse_args()
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    with open(args.file_to_ticker_list, 'r') as file:
        ticker_symbols = file.read().splitlines()
    for ticker_symbol in ticker_symbols:
        fetch_and_save_ticker_data(ticker_symbol, args.output_directory)

if __name__ == "__main__":
    main()
