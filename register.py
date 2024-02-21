from selenium import webdriver
from selenium.webdriver.common.by import By
import random, string

BASE_URL = 'https://www.investopedia.com/simulator/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(1)
driver.maximize_window()

driver.get(BASE_URL)
login_button = driver.find_element(By.CSS_SELECTOR, "button[data-cy='landing-page-hero-registration-button']")
login_button.click()
email_input = driver.find_element(By.ID, "email")
username_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")
password_confirm_input = driver.find_element(By.ID, "password-confirm")
submit_button = driver.find_element(By.ID, "register")

email_input.send_keys("")
username_input.send_keys("" + ''.join(random.choices(string.ascii_letters + string.digits, k=8)))
password_input.send_keys("")
password_confirm_input.send_keys("")
submit_button.click()
