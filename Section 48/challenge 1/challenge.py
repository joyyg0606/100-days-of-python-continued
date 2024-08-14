from browser_setup import setup_driver
from selenium.webdriver.common.by import By

driver = setup_driver()

# Navigate to the (fake) newsletter registration page
driver.get("https://secure-retreat-92358.herokuapp.com/")

# Find and fill out the form fields
driver.find_element(By.NAME, "fName").send_keys("Angela")
driver.find_element(By.NAME, "lName").send_keys("Yu")
driver.find_element(By.NAME, "email").send_keys("angela@email.com")

# Locate the "Sign Up" button and click on it
driver.find_element(By.CSS_SELECTOR, "form button").click()