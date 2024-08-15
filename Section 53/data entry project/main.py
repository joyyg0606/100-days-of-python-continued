from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Part 1 - Scrape the links, addresses, and prices of the rental properties

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

try:
    # Fetch the webpage
    response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all the property links
    all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
    all_links = [link["href"] if "http" in link["href"] else f"https://appbrewery.github.io{link['href']}" for link in all_link_elements]
    
    # Extract all the addresses
    all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
    all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address_elements]

    # Extract all the prices
    all_price_elements = soup.select(".PropertyCardWrapper span")
    all_prices = [price.get_text().replace("/mo", "").split("+")[0].strip() for price in all_price_elements if "$" in price.get_text()]

    # Ensure the number of extracted data points match
    if not (len(all_links) == len(all_addresses) == len(all_prices)):
        raise ValueError("Mismatch in the number of links, addresses, and prices")

    print(f"There are {len(all_links)} links to individual listings:\n{all_links}")
    print(f"There are {len(all_addresses)} addresses:\n{all_addresses}")
    print(f"There are {len(all_prices)} prices:\n{all_prices}")

except requests.RequestException as e:
    print(f"Error while making the request: {e}")
    exit()

# Part 2 - Fill in the Google Form using Selenium

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Use the try-finally block to ensure the browser gets closed after execution
try:
    for i in range(len(all_links)):
        try:
            # Open Google Form
            driver.get("YOUR_GOOGLE_FORM_LINK_HERE")

            # Use WebDriverWait for dynamic waits rather than static time.sleep()
            wait = WebDriverWait(driver, 10)

            # Locate the form fields
            address_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
            price_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
            link_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')))

            # Fill in the form fields
            address_field.send_keys(all_addresses[i])
            price_field.send_keys(all_prices[i])
            link_field.send_keys(all_links[i])
            submit_button.click()

            # Wait for the form to be submitted before proceeding
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred during form submission: {e}")
finally:
    # Close the browser after all operations are complete
    driver.quit()