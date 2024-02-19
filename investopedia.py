from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import chromedriver_autoinstaller
from dotenv import load_dotenv
import os, time, random, json
from enum import Enum

load_dotenv()
chromedriver_autoinstaller.install()

api_email = os.getenv("API_EMAIL")
api_password = os.getenv("API_PASSWORD")

class TradeAction(Enum):
    BUY = 0
    SELL = 1
    SHORT = 2
    SELL_TO_COVER = 3

class TradeOrderType(Enum):
    LIMIT = 0
    MARKET = 1
    STOP_LIMIT = 2

class TradeDuration(Enum):
    DAY_ONLY = 0
    GOOD_UNTIL_CANCELLED = 1

class LoginError(Exception):
    def __init__(self, alert):
        super().__init__(f"Login Error: {alert.text}")

class InvestopediaAPI:
    BASE_URL = 'https://www.investopedia.com/simulator'

    def __init__(self, email, password):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

        self.driver.get(self.BASE_URL)
        login_button = self.driver.find_element(By.XPATH, "//button[@title='Log in to your account']")
        login_button.click()
        email_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "login")
        email_input.send_keys(api_email)
        password_input.send_keys(api_password)
        time.sleep(random.random())
        submit_button.click()

        try:
            alert = self.driver.find_element(By.CLASS_NAME, "alert")
            raise LoginError(alert)
        except NoSuchElementException:
            return

    def trade(self, symbol, action, quantity, order_type, duration):
        self.driver.get(self.BASE_URL + "/trade/stocks")
        symbol_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Look up Symbol/Company Name']")
        symbol_input.send_keys(symbol)
        symbol_result = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@data-cy='symbol-name']")))
        
        if symbol_result.text == symbol:
            symbol_result.click()
        else:
            return False
        
        transaction_form = self.driver.find_element(By.CLASS_NAME, "trade-transaction-form")
        action_select, _, order_type_select, duration_select = transaction_form.find_elements(By.CLASS_NAME, "v-input__control")

        action_select.click()
        action_list = self.driver.find_elements(By.XPATH, "//div[@role='listbox']")[1]
        actions = action_list.find_elements(By.CLASS_NAME, "v-list-item")
        actions[action.value].click()

        quantity_input = self.driver.find_element(By.CSS_SELECTOR, "input[data-cy='quantity-input']")
        quantity_input.send_keys(str(quantity))

        order_type_select.click()
        order_type_list = self.driver.find_elements(By.XPATH, "//div[@role='listbox']")[2]
        order_types = order_type_list.find_elements(By.CLASS_NAME, "v-list-item")
        order_types[order_type.value].click()

        duration_select.click()
        duration_list = self.driver.find_elements(By.XPATH, "//div[@role='listbox']")[3]
        durations = duration_list.find_elements(By.CLASS_NAME, "v-list-item")
        durations[duration.value].click()

        preview_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-cy='preview-button']")
        preview_button.click()
        time.sleep(1)
        sumbit_order_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-cy='submit-order-button']")
        sumbit_order_button.click()

    def get_pending_trades(self):
        self.driver.get(self.BASE_URL + "/portfolio")

        pending_trades = self.driver.find_elements(By.CSS_SELECTOR, "div[data-cy='pending-table-row']")
        ret = []

        for pending_trade in pending_trades:
            symbol = pending_trade.find_element(By.CSS_SELECTOR, "div[data-cy='symbol-value']")
            description = pending_trade.find_element(By.CSS_SELECTOR, "div[data-cy='description-value']")
            transaction = pending_trade.find_element(By.CSS_SELECTOR, "div[data-cy='transaction-value']")
            quantity = pending_trade.find_element(By.CSS_SELECTOR, "div[data-cy='quantity-value']")
            current_price = pending_trade.find_element(By.CSS_SELECTOR, "div[data-cy='current-price-value']")
            ret.append({
                "Symbol": symbol.text,
                "Description": description.text,
                "Transaction": transaction.text,
                "Quantity": quantity.text,
                "Current Price": current_price.text
            })

        return json.dumps(ret, indent=4)
