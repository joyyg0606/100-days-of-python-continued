import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "LON"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    flight_data = find_cheapest_flight(
        flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today
        )
    )
    if flight_data.price != "N/A" and flight_data.price < destination["lowestPrice"]:
        message = (f"Low price alert! Only £{flight_data.price} to fly from "
                   f"{flight_data.origin_airport} to {flight_data.destination_airport}, "
                   f"from {flight_data.out_date} to {flight_data.return_date}. "
                   f"Number of stops: {flight_data.stops}.")

        notification_manager.send_sms(message_body=message)
        notification_manager.send_whatsapp(message_body=message)

        user_data = data_manager.get_customer_emails()
        emails = [user["email"] for user in user_data]
        notification_manager.send_emails(email_list=emails, email_body=message)

    time.sleep(1)  # To avoid hitting rate limits