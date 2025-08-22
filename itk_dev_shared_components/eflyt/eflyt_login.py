"""Module for logging into Eflyt using Selenium"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


class ResilientBrowser(webdriver.Chrome):
    """A webdriver.Chrome subclass that retries find_element if the element goes stale."""
    def find_element(self, by=By.ID, value = None) -> WebElement:
        element = super().find_element(by, value)
        time.sleep(0.1)
        try:
            element.tag_name
        except StaleElementReferenceException:
            element = super().find_element(by, value)
        return element


def login(username: str, password: str) -> ResilientBrowser:
    """Log into Eflyt using a password and username.

    Args:
        username: Username for login.
        password: Password for login.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    browser = ResilientBrowser(options=chrome_options)
    browser.maximize_window()
    browser.implicitly_wait(2)

    browser.get("https://notuskommunal.scandihealth.net/")
    browser.find_element(By.ID, "Login1_UserName").send_keys(username)
    browser.find_element(By.ID, "Login1_Password").send_keys(password)
    browser.find_element(By.ID, "Login1_LoginImageButton").click()

    try:
        browser.find_element(By.ID, "ctl00_imgLogo")
    except NoSuchElementException as exc:
        raise RuntimeError("Login failed") from exc

    return browser
