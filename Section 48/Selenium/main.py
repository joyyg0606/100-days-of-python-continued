from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Chrome options to keep the browser open
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Set up the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

def test_eight_components():
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    # Verify page title
    title = driver.title
    assert title == "Web form"

    # Use implicit wait
    driver.implicitly_wait(10)

    # Locate and interact with web elements
    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    text_box.send_keys("Selenium")
    submit_button.click()

    # Verify the success message
    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"

    # Close the browser window
    driver.quit()

test_eight_components()