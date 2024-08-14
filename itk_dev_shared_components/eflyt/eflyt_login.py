"""Module for logging into Eflyt/Daedalus/Whatchamacallit using Selenium"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def login(username: str, password: str) -> webdriver.Chrome:
    """Log into Eflyt using a password and username.

    Args:
        username: Username for login.
        password: Password for login.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()

    browser.get("https://notuskommunal.scandihealth.net/")
    browser.find_element(By.ID, "Login1_UserName").send_keys(username)
    browser.find_element(By.ID, "Login1_Password").send_keys(password)
    browser.find_element(By.ID, "Login1_LoginImageButton").click()

    try:
        browser.find_element(By.ID, "ctl00_imgLogo")
    except NoSuchElementException as exc:
        raise RuntimeError("Login failed") from exc

    return browser
