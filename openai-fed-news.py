from openai import OpenAI
import datetime

client = OpenAI()
print("AskGPT")


def unix_to_datetime(unix_timestamp):
    return datetime.datetime.utcfromtimestamp(unix_timestamp).strftime('%d-%m-%Y')


# Get the current UNIX timestamp
current_time = datetime.datetime.now().timestamp()
file_name = unix_to_datetime(current_time) + "_news.txt"

with open(file_name, 'r') as file:
    input_text = file.read()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a stock advisor, I give you current data from news market. You output 5 stock recommendations based on this input. Only the 5 stocks, say nothing else."},
        {"role": "user", "content": input_text},
    ]
)

response = completion.choices[0].message.content

with open("StockRecommendations.txt", 'w') as file:
    file.write(response)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a stock advisor. Translate I give you current data from news market. You output 5 stock recommendations based on this input. Only the 5 stocks, say nothing else."},
        {"role": "user", "content": response},
    ]
)
response = completion.choices[0].message.content
with open("StockRecommendations.txt", 'w') as file:
    file.write(response)
