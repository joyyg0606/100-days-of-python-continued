from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


SIMILAR_ACCOUNT = "buzzfeedtasty"  # Change this to an account of your choice
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"


class InstaFollower:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def wait_for_element(self, by, value, timeout=10):
        """ Wait for element to appear for the specified timeout """
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                return self.driver.find_element(by=by, value=value)
            except NoSuchElementException:
                time.sleep(0.5)
        raise NoSuchElementException(f"Element not found: {value}")

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)  # Adjust this based on your connection

        try:
            # Handling cookie consent
            decline_cookies_xpath = "//button[contains(text(), 'Only allow essential cookies')]"
            cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
            if cookie_warning:
                cookie_warning[0].click()
        except NoSuchElementException:
            pass

        username = self.wait_for_element(By.NAME, "username")
        password = self.wait_for_element(By.NAME, "password")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        time.sleep(2)
        password.send_keys(Keys.ENTER)

        # Dismiss prompts after login
        self.dismiss_save_login_info()
        self.dismiss_notifications()

    def dismiss_save_login_info(self):
        try:
            save_login_prompt = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            save_login_prompt.click()
        except NoSuchElementException:
            pass

    def dismiss_notifications(self):
        try:
            notifications_prompt = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            notifications_prompt.click()
        except NoSuchElementException:
            pass

    def find_followers(self):
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers")
        time.sleep(8)

        modal_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]"
        modal = self.wait_for_element(By.XPATH, modal_xpath)
        
        for _ in range(5):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow(self):
        try:
            all_buttons = self.driver.find_elements(By.CSS_SELECTOR, '._aano button')

            for button in all_buttons:
                try:
                    if button.text == "Follow":
                        button.click()
                        time.sleep(1.1)
                except ElementClickInterceptedException:
                    cancel_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
                    cancel_button.click()
        except NoSuchElementException as e:
            print(f"Error finding buttons: {e}")

    def close_browser(self):
        self.driver.quit()


if __name__ == "__main__":
    bot = InstaFollower()
    try:
        bot.login()
        bot.find_followers()
        bot.follow()
    finally:
        bot.close_browser()