import time
from datetime import datetime, timedelta

import pytest as pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

SITE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"
TRANSACTIONS_BUTTON_XPATH = "//button[contains(text(), 'Transactions')]"
CUSTOMER_LOGIN_BUTTON_XPATH = "//button[contains(text(), 'Customer Login')]"
USER_SELECT_ID = "userSelect"
LOGIN_BUTTON_CLASS_NAME = "btn-default"
DEPOSIT_BUTTON_XPATH = "//button[contains(text(), 'Deposit')]"
DEPOSIT_INPUT_SELECTOR = ".form-group input"
SET_DEPOSIT_BUTTON_SELECTOR = ".btn.btn-default"
WITHDRAW_BUTTON_SELECTOR = ".btn.btn-lg.tab:nth-child(3)"
WITHDRAW_INPUT_SELECTOR = 'input[type="number"]'
SET_WITHDRAW_SELECTOR = "button.btn.btn-default"
BACK_BUTTON_SELECTOR = ".fixedTopBox .btn"
TRANSACTIONS_TABLE_CLASS_NAME = "table-bordered"
TRANSACTIONS_TABLE_BODY_SELECTOR = "tbody"
TRANSACTION_ROW_TAG = "tr"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def get_transactions(driver):
    table = driver.find_element(By.CLASS_NAME, TRANSACTIONS_TABLE_CLASS_NAME)
    rows = table.find_element(By.CSS_SELECTOR, TRANSACTIONS_TABLE_BODY_SELECTOR)
    tr_elements = rows.find_elements(By.TAG_NAME, TRANSACTION_ROW_TAG)
    return tr_elements


def find_and_click_on_element_by_css_selector(driver, css_selector):
    element = driver.find_element(By.CSS_SELECTOR, css_selector)
    element.click()


def click_on_transactions_button(driver):
    transactions_button = driver.find_element(By.XPATH, TRANSACTIONS_BUTTON_XPATH)
    transactions_button.click()


def login(driver, username):
    customer_login_button = driver.find_element(By.XPATH, CUSTOMER_LOGIN_BUTTON_XPATH)
    customer_login_button.click()
    select_element = Select(driver.find_element(By.ID, USER_SELECT_ID))
    select_element.select_by_visible_text(username)
    login_button = driver.find_element(By.CLASS_NAME, LOGIN_BUTTON_CLASS_NAME)
    login_button.click()


def deposit(driver, amount):
    deposit_action_button = driver.find_element(By.XPATH, DEPOSIT_BUTTON_XPATH)
    deposit_action_button.click()
    amount_input = driver.find_element(By.CSS_SELECTOR, DEPOSIT_INPUT_SELECTOR)
    amount_input.send_keys(amount)
    find_and_click_on_element_by_css_selector(driver, SET_DEPOSIT_BUTTON_SELECTOR)


def withdraw(driver, amount):
    find_and_click_on_element_by_css_selector(driver, WITHDRAW_BUTTON_SELECTOR)
    withdraw_input = driver.find_element(By.CSS_SELECTOR, WITHDRAW_INPUT_SELECTOR)
    withdraw_input.send_keys(amount)
    find_and_click_on_element_by_css_selector(driver, SET_WITHDRAW_SELECTOR)


def click_on_back_button(driver):
    find_and_click_on_element_by_css_selector(driver, BACK_BUTTON_SELECTOR)


def test_transaction_flow(driver):
    driver.get(SITE_URL)
    driver.implicitly_wait(10)
    login(driver, "Harry Potter")
    click_on_transactions_button(driver)
    assert len(get_transactions(driver)) == 0, "Transactions table not empty"
    click_on_back_button(driver)
    deposit(driver, "200")
    withdraw(driver, "100")
    click_on_transactions_button(driver)
    driver.refresh()
    assert len(get_transactions(driver)) == 2, "Test Failed: There are not exactly 2 results."
