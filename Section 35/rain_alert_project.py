import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Constants
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.environ.get("OWM_API_KEY")
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")
TO_NUMBER = os.environ.get("TWILIO_TO_NUMBER")

def get_weather_data():
    """Fetch weather data from OpenWeatherMap API."""
    weather_params = {
        "lat": 46.947975,
        "lon": 7.447447,
        "appid": API_KEY,
        "cnt": 4,  # Number of forecasted time slots (3-hour intervals)
    }
    try:
        response = requests.get(OWM_ENDPOINT, params=weather_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def will_it_rain(weather_data):
    """Check if it will rain based on weather data."""
    for hour_data in weather_data["list"]:
        condition_code = hour_data["weather"][0]["id"]
        if int(condition_code) < 700:
            return True
    return False

def send_rain_alert():
    """Send an SMS alert if rain is expected."""
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ.get('https_proxy')}

    client = Client(ACCOUNT_SID, AUTH_TOKEN, http_client=proxy_client)

    try:
        message = client.messages.create(
            body="It's going to rain today. Remember to bring an ☔️",
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print(f"Message status: {message.status}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def main():
    """Main function to check weather and send alert if needed."""
    weather_data = get_weather_data()
    if weather_data and will_it_rain(weather_data):
        send_rain_alert()
    else:
        print("No rain expected.")

if __name__ == "__main__":
    main()