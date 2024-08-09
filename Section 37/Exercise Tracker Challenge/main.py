import requests
from datetime import datetime
import os

# Your personal data. Used by Nutritionix to calculate calories.
GENDER = "male"
WEIGHT_KG = 84
HEIGHT_CM = 180
AGE = 32

# Nutritionix APP ID and API Key. Actual values are stored as environment variables.
APP_ID = os.getenv("ENV_NIX_APP_ID")
API_KEY = os.getenv("ENV_NIX_API_KEY")

# Ensure environment variables are set
if not APP_ID or not API_KEY:
    raise ValueError("Nutritionix APP_ID or API_KEY environment variables are not set.")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

def get_exercise_data():
    exercise_text = input("Tell me which exercises you did: ")

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
    }

    parameters = {
        "query": exercise_text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    try:
        response = requests.post(exercise_endpoint, json=parameters, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch exercise data: {e}")
        return None

def log_to_sheet(exercises):
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    sheet_endpoint = os.getenv("ENV_SHEETY_ENDPOINT")
    if not sheet_endpoint:
        raise ValueError("Sheety endpoint environment variable is not set.")

    for exercise in exercises:
        sheet_inputs = {
            "workout": {
                "date": today_date,
                "time": now_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

        try:
            # Sheety Authentication Option 2: Basic Auth
            sheet_response = requests.post(
                sheet_endpoint,
                json=sheet_inputs,
                auth=(
                    os.getenv("ENV_SHEETY_USERNAME"),
                    os.getenv("ENV_SHEETY_PASSWORD"),
                )
            )
            sheet_response.raise_for_status()
            print(f"Logged to Google Sheet: {sheet_response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to log to Google Sheet: {e}")

def main():
    exercise_data = get_exercise_data()
    if exercise_data and "exercises" in exercise_data:
        log_to_sheet(exercise_data["exercises"])
    else:
        print("No exercise data to log.")

if __name__ == "__main__":
    main()