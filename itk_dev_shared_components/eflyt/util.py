'''General helper funtions'''
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def format_date(_date: date) -> str:
    '''Format date as %d%m%Y'''
    return _date.strftime("%d-%m-%Y")


def extract_rows(browser: webdriver.Chrome, table_id: str) -> list[WebElement]:
    '''Get rows by ID

    Args:
        browser: The browser app to use
        row_id: The row to extract

    Return:
        A list of WebElements'''
    table = browser.find_element(By.ID, table_id)
    rows = table.find_elements(By.TAG_NAME, "tr")
    # Remove header row
    rows.pop(0)
    return rows


def clear_and_input(browser: webdriver, dom_id: str, input: str):
    from_date_field = browser.find_element(By.ID, dom_id)
    from_date_field.clear()
    from_date_field.send_keys(input)
