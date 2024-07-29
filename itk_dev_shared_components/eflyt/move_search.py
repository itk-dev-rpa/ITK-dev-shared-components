'''Interface for working with the 'Digital Flytning' section of Eflyt'''
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement

from itk_dev_shared_components.eflyt.util import format_date, extract_rows
from itk_dev_shared_components.eflyt.case import Case


ALLOWED_CASE_TYPES = (
    "Logivært",
    "Boligselskab",
    "For sent anmeldt"
)


def move_search(browser: webdriver.Chrome, from_date: date | None = None, to_date: date | None = None, case_state: str = "Alle", case_status: str = "(vælg status)") -> list[WebElement]:
    """Apply the correct filters in Eflyt and search the case list.

    Args:
        browser: The webdriver browser object.
    """
    Select(browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_ddlTilstand")).select_by_visible_text(case_state)
    Select(browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_ddlStatus")).select_by_visible_text(case_status)
    if from_date:
        browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_txtFlytteStartDato").send_keys(format_date(to_date))
    if to_date:
        browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_txtFlytteEndDato").send_keys(format_date(to_date))
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_btnSearch").click()

    return extract_rows(browser, "ctl00_ContentPlaceHolder2_GridViewSearchResult")


def extract_cases(rows: list[WebElement]) -> list[str]:
    """Extract and filter cases from the case table.

    Args:
        browser: The webdriver browser object.

    Returns:
        A list of filtered case objects.
    """
    cases = []
    for row in rows:
        case_number = row.find_element(By.XPATH, "td[4]").text
        case_types_text = row.find_element(By.XPATH, "td[5]").text

        # If the case types ends with '...' we need to get the title instead
        if case_types_text.endswith("..."):
            case_types_text = row.find_element(By.XPATH, "td[5]").get_attribute("Title")

        case_types = case_types_text.split(", ")

        # Check if there are any case types other than the allowed ones
        for case_type in case_types:
            if case_type not in ALLOWED_CASE_TYPES:
                break
        else:
            cases.append(case_number)

    return cases


def open_case(browser: webdriver.Chrome, case: Case):
    """Open a case by searching for it's case number.

    Args:
        browser: The webdriver browser object.
        case: The case to open.
    """
    # The id for both the search field and search button changes based on the current view hence the weird selectors.
    case_input = browser.find_element(By.XPATH, '//input[contains(@id, "earchControl_txtSagNr")]')
    case_input.clear()
    case_input.send_keys(case.case_number)

    browser.find_element(By.XPATH, '//input[contains(@id, "earchControl_btnSearch")]').click()
