import finnhub
import os
import datetime
from dotenv import load_dotenv
from buy_news import unix_to_datetime
import datetime

# Load environment variables from .env file
load_dotenv()

# Access the BUSINESS_API variable
business_api_key = os.getenv("BUSINESS_API")

# Use the business_api_key in your code
finnhub_client = finnhub.Client(
    api_key=business_api_key)

# To Do: Change file name to appropriate one
file_name = "tickers.csv"
with open(file_name, 'r') as file:
    input_text = file.read()

stocks = input_text.split(",")


def get_dates():
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    return today.strftime("%Y-%m-%d"), last_week.strftime("%Y-%m-%d")


# Example usage
today_date, last_week_date = get_dates()

news = []
for stock in stocks:
    news.append(finnhub_client.company_news(stock,
                                            _from=last_week_date, to=today_date))

file_name = "selling_news.txt"
with open(file_name, 'w') as file:
    # Iterate over each news item
    for item in news:
        for item in news:
            # Extract headline, summary, and datetime
            headline = item['headline']
            summary = item['summary']
            news_datetime = unix_to_datetime(item['datetime'])

            # Write headline, summary, and datetime to the file
            file.write(f"{news_datetime}\n")
            file.write(f"Headline: {headline}\n")
            file.write(f"Summary: {summary}\n")
            file.write("\n")  # Add a newline for separation between news items

print(finnhub_client.company_news('AAPL', _from="2024-02-02", to="2024-02-10"))
