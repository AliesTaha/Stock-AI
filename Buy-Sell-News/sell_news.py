import finnhub
finnhub_client = finnhub.Client(
    api_key="cn9e659r01qoee9a1n10cn9e659r01qoee9a1n1g")

print(finnhub_client.company_news('AAPL', _from="2024-02-02", to="2024-02-10"))
