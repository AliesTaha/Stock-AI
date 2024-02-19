import finnhub
import datetime

# Initialize the Finnhub client
finnhub_client = finnhub.Client(
    api_key="cn9e659r01qoee9a1n10cn9e659r01qoee9a1n1g")

# Get the current UNIX timestamp
current_time = datetime.datetime.now().timestamp()

# Retrieve general news with a minimum ID of 0
news = finnhub_client.general_news('general', min_id=0)

# Define a function to convert UNIX timestamp to day/month/year format


def unix_to_datetime(unix_timestamp):
    return datetime.datetime.utcfromtimestamp(unix_timestamp).strftime('%d-%m-%Y')


# Create a file with the current date and time as the filename
file_name = unix_to_datetime(current_time) + "_news.txt"

# Open the file in write mode
with open(file_name, 'w') as file:
    # Iterate over each news item
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

# Print a message indicating the file has been created
