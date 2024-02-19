import yfinance as yf
from datetime import datetime, timedelta
import argparse
import os

def fetch_and_save_ticker_data(ticker_symbol, output_directory):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)
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
