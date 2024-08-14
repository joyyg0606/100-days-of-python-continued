from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# Navigate to the game
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Get the cookie element
cookie = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "cookie"))
)

# Get upgrade item ids
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5 minutes

logging.basicConfig(level=logging.INFO)

while True:
    cookie.click()

    # Every 5 seconds:
    if time.time() > timeout:
        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")

        # Convert <b> text into an integer price and construct the upgrades dictionary
        cookie_upgrades = {
            int(price.text.split("-")[1].strip().replace(",", "")): item_ids[idx]
            for idx, price in enumerate(all_prices)
            if price.text
        }

        # Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        cookie_count = int(money_element.replace(",", "")) if money_element else 0

        # Find upgrades that we can currently afford
        affordable_upgrades = {
            cost: id for cost, id in cookie_upgrades.items() if cookie_count >= cost
        }

        if affordable_upgrades:
            # Purchase the most expensive affordable upgrade
            highest_price_affordable_upgrade = max(affordable_upgrades)
            to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

            driver.find_element(By.ID, to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes, stop the bot and check the cookies per second count
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        logging.info(f"Cookies per second: {cookie_per_s}")
        break