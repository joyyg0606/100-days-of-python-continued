import requests
from datetime import datetime
import os

# It's better to store sensitive information in environment variables
USERNAME = os.getenv("PIXELA_USERNAME", "YOUR USERNAME")
TOKEN = os.getenv("PIXELA_TOKEN", "YOUR SELF GENERATED TOKEN")
GRAPH_ID = os.getenv("PIXELA_GRAPH_ID", "YOUR GRAPH ID")

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# Example of creating a user (uncomment if needed)
# response = requests.post(url=pixela_endpoint, json=user_params)
# if response.ok:
#     print("User created successfully.")
# else:
#     print("Failed to create user:", response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# Example of creating a graph (uncomment if needed)
# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# if response.ok:
#     print("Graph created successfully.")
# else:
#     print("Failed to create graph:", response.text)

# Common date formatting stored in a variable to avoid repetition
today_date = datetime.now().strftime("%Y%m%d")

pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

# Input validation for kilometers cycled
while True:
    try:
        quantity = float(input("How many kilometers did you cycle today? "))
        break
    except ValueError:
        print("Please enter a valid number.")

pixel_data = {
    "date": today_date,
    "quantity": str(quantity),
}

response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
if response.ok:
    print("Pixel created successfully.")
else:
    print("Failed to create pixel:", response.text)

update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today_date}"

new_pixel_data = {
    "quantity": "4.5"
}

# Example of updating a pixel (uncomment if needed)
# response = requests.put(url=update_endpoint, json=new_pixel_data, headers=headers)
# if response.ok:
#     print("Pixel updated successfully.")
# else:
#     print("Failed to update pixel:", response.text)

delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today_date}"