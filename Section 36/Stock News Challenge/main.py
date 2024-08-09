import os
import requests
from twilio.rest import Client

# Constants
VIRTUAL_TWILIO_NUMBER = os.environ.get("TWILIO_VIRTUAL_NUMBER")
VERIFIED_NUMBER = os.environ.get("TWILIO_VERIFIED_NUMBER")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# Function to get stock data
def get_stock_data(stock_name):
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_name,
        "apikey": STOCK_API_KEY,
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    response.raise_for_status()
    return response.json()["Time Series (Daily)"]

# Function to calculate percentage difference
def calculate_difference(data):
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    day_before_yesterday_data = data_list[1]

    yesterday_closing_price = float(yesterday_data["4. close"])
    day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

    difference = yesterday_closing_price - day_before_yesterday_closing_price
    up_down = "🔺" if difference > 0 else "🔻"
    diff_percent = round((difference / yesterday_closing_price) * 100, 2)

    return up_down, diff_percent

# Function to get news articles
def get_news(company_name):
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": company_name,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    return articles[:3]

# Function to send SMS via Twilio
def send_sms(messages):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for message in messages:
        sms = client.messages.create(
            body=message,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
        print(f"Message sent with SID: {sms.sid}")

# Main function
def main():
    try:
        stock_data = get_stock_data(STOCK_NAME)
        up_down, diff_percent = calculate_difference(stock_data)

        if abs(diff_percent) > 5:
            articles = get_news(COMPANY_NAME)
            formatted_articles = [
                f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}\nBrief: {article['description']}" 
                for article in articles
            ]
            send_sms(formatted_articles)
        else:
            print("No significant change in stock price.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()