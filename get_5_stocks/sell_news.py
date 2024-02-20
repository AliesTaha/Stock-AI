import finnhub
import os
import datetime
from dotenv import load_dotenv
from buy_news import unix_to_datetime
import datetime
# Load environment variables from .env file
load_dotenv()
current_time = datetime.datetime.now().timestamp()

# Access the BUSINESS_API variable
business_api_key = os.getenv("BUSINESS_API")

# Use the business_api_key in your code
finnhub_client = finnhub.Client(
    api_key=business_api_key)

# To Do: Change file name to appropriate one
file_name = "tickers_to_buy.csv"
with open(file_name, 'r') as file:
    input_text = file.read()

stocks = input_text.split(",")

# Dictionary to keep track of headlines count per stock per day
headline_counts = {stock: {} for stock in stocks}


def get_dates():
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    return today.strftime("%Y-%m-%d"), last_week.strftime("%Y-%m-%d")


# Example usage
today_date, last_week_date = get_dates()

file_name = unix_to_datetime(current_time)+"_selling_news.txt"
with open(file_name, 'w') as file:
    for i in range(len(stocks)):
        news = finnhub_client.company_news(
            stocks[i], _from=last_week_date, to=today_date)

        # Iterate over each news item
        for item in news:
            # Extract headline, summary, and datetime
            headline = item['headline']
            summary = item['summary']
            news_datetime = unix_to_datetime(item['datetime'])

            # Check if the count for this stock on this day exceeds 15
            if headline_counts[stocks[i]].get(news_datetime, 0) >= 6:
                continue  # Skip adding this headline

            # Update the count of headlines for this stock on this day
            headline_counts[stocks[i]][news_datetime] = headline_counts[stocks[i]].get(
                news_datetime, 0) + 1

            # Write headline, summary, and datetime to the file
            file.write(f"{news_datetime}\n")
            file.write(f"Headline: {headline}\n")
            file.write(f"Summary: {summary}\n")
            file.write("\n")  # Add a newline for separation between news items
        # Add a newline for separation between news items
        file.write("---------------------NEXT STOCK---------------------\n")
