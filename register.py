import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import random, string, time

parser = argparse.ArgumentParser(description="Automate registration on Investopedia Simulator")
parser.add_argument("--email", required=True, help="Email address for registration")
parser.add_argument("--username", required=True, help="Username for registration")
parser.add_argument("--password", required=True, help="Password for registration")

args = parser.parse_args()

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

email_input.send_keys(args.email)
username_input.send_keys(args.username + "".join(random.choices(string.ascii_letters + string.digits, k=8)))
password_input.send_keys(args.password)
password_confirm_input.send_keys(args.password)
time.sleep(random.random())
submit_button.click()
