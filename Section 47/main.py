from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# URL of the product page on Amazon
url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

# Minimal header to make the request look like it comes from a browser
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

try:
    # Adding headers to the request
    response = requests.get(url, headers=header)
    response.raise_for_status()  # Raise an HTTPError for bad responses
except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve the webpage: {e}")
    exit()

soup = BeautifulSoup(response.content, "html.parser")

# Check you are getting the actual Amazon page back and not something else:
print(soup.prettify())

try:
    # Find the HTML element that contains the price
    price = soup.find(class_="a-offscreen").get_text()
    # Remove the dollar sign and convert to float
    price_as_float = float(price.split("$")[1])
    print(price_as_float)

    # Get the product title
    title = soup.find(id="productTitle").get_text().strip()
    print(title)
except AttributeError as e:
    print(f"Error parsing the page: {e}")
    exit()

# Set the price below which you would like to get a notification
BUY_PRICE = 70

if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"

    try:
        # ====================== Send the email ===========================
        with smtplib.SMTP(os.getenv("SMTP_ADDRESS"), port=587) as connection:
            connection.starttls()
            connection.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            connection.sendmail(
                from_addr=os.getenv("EMAIL_ADDRESS"),
                to_addrs=os.getenv("EMAIL_ADDRESS"),
                msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
            )
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")