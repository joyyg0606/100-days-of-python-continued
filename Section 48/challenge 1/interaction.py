from browser_setup import setup_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = setup_driver()

try:
    # Navigate to Wikipedia
    driver.get("https://en.wikipedia.org/wiki/Main_Page")

    # Find and click elements
    article_count = driver.find_element(By.CSS_SELECTOR, "#articlecount a")
    # article_count.click()

    all_portals = driver.find_element(By.LINK_TEXT, "Content portals")
    # all_portals.click()

    # Perform a search
    search = driver.find_element(By.NAME, "search")
    search.send_keys("Python", Keys.ENTER)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()