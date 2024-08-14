from browser_setup import setup_driver
from selenium.webdriver.common.by import By

driver = setup_driver()

# Navigate to Python.org
driver.get("https://www.python.org/")

# Search for events
event_times = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
event_names = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")

events = [{"time": time.text, "name": name.text} for time, name in zip(event_times, event_names)]
for event in events:
    print(event)

driver.quit()