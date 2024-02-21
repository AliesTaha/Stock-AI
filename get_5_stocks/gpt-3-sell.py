import os
from openai import OpenAI
import datetime

client = OpenAI()


def unix_to_datetime(unix_timestamp):
    return datetime.datetime.utcfromtimestamp(unix_timestamp).strftime('%d-%m-%Y')


# Get the current UNIX timestamp
current_time = datetime.datetime.now().timestamp()
file_name = unix_to_datetime(current_time) + "_selling_news.txt"

# Check if today's file exists, if not, get yesterday's file name
if not os.path.isfile(str(file_name)):
    # Subtracting 24 hours in seconds
    yesterday_time = current_time - (24 * 60 * 60)
    file_name = unix_to_datetime(yesterday_time) + "_selling_news.txt"

with open(file_name, 'r') as file:
    input_text = file.read()

file_name = "stocks_to_buy.txt"
with open(file_name, 'r') as file:
    input_text_2 = file.read()
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a stock advisor, I give you current data from news market. You output which stock I HAVE TO SELL FOR MY BENEFIT, in order from MUST SELL TO MAYBE SELL to LEAST Sell, top to bottom. Recommendations based on this input. Only output the stock company names, say nothing else. Make sure company names are from list allowed by user."},
        {"role": "user", "content": input_text +
            "your options are the following stocks"+input_text_2+"don't output any other, you're only allowed to reorder above stocks"},
    ]
)

response = completion.choices[0].message.content

with open("stocks_to_sell.txt", 'w') as file:
    file.write(response)

with open(file_name, 'r') as file:
    input_text = file.read()

stocks = input_text.split(",")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a stock advisor. Output the stock ticker symbols only, no names, no numbers in the front of the bullet points"},
        {"role": "user", "content": response},
    ]
)
response2 = completion.choices[0].message.content
# Concatenate ticker symbols with commas
ticker_symbols = ",".join(response2.split())
final = []
i = 0
while i < (len(ticker_symbols))-1:
    if ticker_symbols[i] == '-':
        i += 2
    else:
        final.append(ticker_symbols[i])
        i += 1
with open("tickers_to_sell.csv", 'w') as file:
    file.write("".join(final))
