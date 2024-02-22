from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller
from dotenv import load_dotenv
import os, time, random, json
from enum import Enum
import argparse

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
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
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=chrome_options)
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

        try:
            dialog = self.driver.find_element(By.XPATH, '//div[@role="dialog"]')
            time.sleep(2)
            dialog.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)
        except NoSuchElementException:
            pass
        
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

        try:
            dialog = self.driver.find_element(By.XPATH, '//div[@role="dialog"]')
            time.sleep(2)
            dialog.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)
        except NoSuchElementException:
            pass

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
    
    def get_holdings(self):
        self.driver.get(self.BASE_URL + "/portfolio")

        try:
            dialog = self.driver.find_element(By.XPATH, '//div[@role="dialog"]')
            time.sleep(2)
            dialog.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)
        except NoSuchElementException:
            pass

        holdings_table = self.driver.find_element(By.CSS_SELECTOR, "div[data-cy='holdings-table']")
        holdings = holdings_table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        ret = []

        for holding in holdings:
            symbol = holding.find_element(By.CSS_SELECTOR, "a > span")
            description = holding.find_element(By.CSS_SELECTOR, "div[data-cy='description']")
            current_price = holding.find_element(By.CSS_SELECTOR, "div[data-cy='current-price']")
            day_gain_loss = holding.find_element(By.CSS_SELECTOR, "div[data-cy='day-gain-dollar']").find_element(By.TAG_NAME, "div")
            purchase_price = holding.find_element(By.CSS_SELECTOR, "div[data-cy='purchase-price']")
            quantity = holding.find_element(By.CSS_SELECTOR, "div[data-cy='quantity']")
            total_value = holding.find_element(By.CSS_SELECTOR, "div[data-cy='total-value']")
            total_gain_loss = holding.find_element(By.CSS_SELECTOR, "div[data-cy='total-gain-dollar']").find_element(By.TAG_NAME, "div")

            day_gain_loss = day_gain_loss.text.split("\n")
            day_gain_dollar = day_gain_loss[0]
            day_gain_percentage = day_gain_loss[1][1:-1]

            total_gain_loss = total_gain_loss.text.split("\n")
            total_gain_dollar = total_gain_loss[0]
            total_gain_percentage = total_gain_loss[1][1:-1]
            ret.append({
                "Symbol": symbol.text,
                "Description": description.text,
                "Current Price": current_price.text,
                "Dollar Day Gain/Loss": day_gain_dollar,
                "Percentage Day Gain/Loss": day_gain_percentage,
                "Purchase Price": purchase_price.text,
                "Quantity": quantity.text,
                "Total Value": total_value.text,
                "Dollar Total Gain/Loss": total_gain_dollar,
                "Percentage Total Gain/Loss": total_gain_percentage,
            })

        return json.dumps(ret, indent=4)
    
    def get_portfolio_status(self):
        self.driver.get(self.BASE_URL + "/portfolio")

        try:
            dialog = self.driver.find_element(By.XPATH, '//div[@role="dialog"]')
            time.sleep(2)
            dialog.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)
        except NoSuchElementException:
            pass

        total_value = self.driver.find_element(By.CSS_SELECTOR, "div[data-cy='total-value']")
        day_change_value = self.driver.find_element(By.CSS_SELECTOR, "div[data-cy='day-change-value']").find_element(By.TAG_NAME, "div").text.split(" ")
        total_change_value =self.driver.find_element(By.CSS_SELECTOR, "div[data-cy='total-change-value']").find_element(By.TAG_NAME, "div").text.split(" ")
        ret = {}
        ret["Total Value"] = total_value.text
        ret["Day Dollar Gain/Loss"] = day_change_value[0]
        ret["Day Percentage Gain/Loss"] = day_change_value[1][1:-1]
        ret["Total Dollar Gain/Loss"] = total_change_value[0]
        ret["Total Percentage Gain/Loss"] = total_change_value[1][1:-1]

        return json.dumps(ret, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Investopedia API Tool")
    
    parser.add_argument("--operation", choices=["trade", "get_pending_trades", "get_holdings", "get_portfolio_status"], help="The operation to perform.")
    
    parser.add_argument("--symbol", help="The symbol for trading.")
    parser.add_argument("--action", choices=["buy", "sell", "short", "sell_to_cover"], help="The action for trading: buy, sell, short, sell_to_cover.")
    parser.add_argument("--quantity", type=int, help="The quantity for trading.")
    
    parser.add_argument("--order_type", choices=["limit", "market", "stop_limit"], help="The order type: limit, market, stop_limit.")
    parser.add_argument("--duration", choices=["day_only", "good_until_cancelled"], help="The duration: day_only, good_until_cancelled.")
    
    args = parser.parse_args()
    
    action_mapping = {
        "buy": TradeAction.BUY,
        "sell": TradeAction.SELL,
        "short": TradeAction.SHORT,
        "sell_to_cover": TradeAction.SELL_TO_COVER
    }
    
    order_type_mapping = {
        "limit": TradeOrderType.LIMIT,
        "market": TradeOrderType.MARKET,
        "stop_limit": TradeOrderType.STOP_LIMIT
    }
    
    duration_mapping = {
        "day_only": TradeDuration.DAY_ONLY,
        "good_until_cancelled": TradeDuration.GOOD_UNTIL_CANCELLED
    }
    
    client = InvestopediaAPI(api_email, api_password)
    
    if args.operation == "trade":
        if args.symbol and args.action and args.quantity and args.order_type and args.duration:
            action = action_mapping[args.action]
            order_type = order_type_mapping[args.order_type]
            duration = duration_mapping[args.duration]
            client.trade(args.symbol, action, args.quantity, order_type, duration)
        else:
            print("Missing required arguments for trading.")
    elif args.operation == "get_pending_trades":
        print(client.get_pending_trades())
    elif args.operation == "get_holdings":
        print(client.get_holdings())
    elif args.operation == "get_portfolio_status":
        print(client.get_portfolio_status())
    else:
        print("Invalid operation or no operation specified.")

