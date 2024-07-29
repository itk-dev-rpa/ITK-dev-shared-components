'''Interface for the Super Search section of Eflyt'''
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from itk_dev_shared_components.eflyt.util import format_date, extract_rows


def super_search(browser: webdriver.Chrome, date_from: date, date_to: date, case_number: str = "", cpr_number: str = "", cvr_number: str = "", address: str = "") -> list[WebElement]:
    """Search for a case and open it.

    Args:
        browser: The browser object.
        case_number: The case number to search for.
    """
    if not case_number and not cpr_number and not cvr_number and not address:
        raise ValueError("No relevant search query entered")
    browser.get("https://notuskommunal.scandihealth.net/web/Supersearch.aspx")
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_imgLogo").click()
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_btnClear").click()
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_txtCprNr").send_keys(cpr_number)
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_txtcvr").send_keys(cvr_number)
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_txtSagNr").send_keys(case_number)
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_adresse").send_keys(address)
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_txtdatoFra").send_keys(format_date(date_from))
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_txtdatoTo").send_keys(format_date(date_to))
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_searchControl_btnSearch").click()
    browser.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$searchControl$GridViewSearchResult','cmdRowSelected$0')")

    return extract_rows(browser, "ctl00_ContentPlaceHolder2_GridViewMovingPersons")


def open_cpr(cpr_in: str, elements: list[WebElement]):
    '''Click a specific CPR in the list

    Args:
        cpr_in: The CPR to look for
        elements: A list of elements
    '''
    for row in elements:
        cpr_link = row.find_element(By.XPATH, "td[2]/a[2]")
        cpr = cpr_link.text.replace("-", "")

        if cpr == cpr_in:
            cpr_link.click()
            break
