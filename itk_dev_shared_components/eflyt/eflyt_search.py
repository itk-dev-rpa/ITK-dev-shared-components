"""Interface for working with the 'Digital Flytning' section of Eflyt"""
from datetime import date, datetime
from typing import Literal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from itk_dev_shared_components.eflyt.eflyt_util import format_date
from itk_dev_shared_components.eflyt.eflyt_case import Case

CaseState = Literal[
    "Alle",
    "Afsluttet",
    "Fraflytning",
    "I gang",
    "Ubehandlet"
]
CaseStatus = Literal[
    "(vælg status)",
    "Afsluttet",
    "Afventer CPR",
    "Afvist",
    "Fejl",
    "Godkendt",
    "I gang",
    "Partshøring",
    "Sendt til CPR",
    "Svarfrist overskredet",
    "Ubehandlet"
]


def search(browser: webdriver.Chrome, from_date: date | None = None, to_date: date | None = None, case_state: CaseState = "Alle", case_status: CaseStatus = "(vælg status)"):
    """Apply the correct filters in Eflyt and search the case list.

    Args:
        browser: The webdriver browser object.
    """
    browser.get("https://notuskommunal.scandihealth.net/web/SearchResulteFlyt.aspx")
    Select(browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_ddlTilstand")).select_by_visible_text(case_state)
    Select(browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_ddlStatus")).select_by_visible_text(case_status)
    if from_date:
        browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_txtFlytteStartDato").send_keys(format_date(from_date))
    if to_date:
        browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_SearchControl_txtFlytteEndDato").send_keys(format_date(to_date))
    browser.find_element(By.XPATH, '//input[contains(@id, "earchControl_btnSearch")]').click()


def extract_cases(browser: webdriver.Chrome) -> list[Case]:
    """Extract and filter cases from the case table. Requires a search to have been performed immediately before.

    Args:
        browser: The webdriver browser object.

    Returns:
        A list of filtered case objects.
    """
    table = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_GridViewSearchResult")
    rows = table.find_elements(By.TAG_NAME, "tr")
    headlines = rows[0].text.split(" ")

    # Remove header row
    rows.pop(0)
    cases = []
    for row in rows:
        deadline = None
        if "Deadline" in headlines:
            deadline_text = row.find_element(By.XPATH, f"td[{headlines.index('Deadline') + 1}]/a").text
            # Convert deadline to date object
            if len(deadline_text) > 0:
                deadline = datetime.strptime(deadline_text, "%d-%m-%Y")

        case_number = row.find_element(By.XPATH, f"td[{headlines.index('Sagsnr.') + 1}]").text
        case_types_text = row.find_element(By.XPATH, f"td[{headlines.index('Flyttetype') + 1}]").text

        # If the case types ends with '...' we need to get the title instead
        if case_types_text.endswith("..."):
            case_types_text = row.find_element(By.XPATH, f"td[{headlines.index('Flyttetype') + 1}]").get_attribute("Title")
        case_types = case_types_text.split(", ")

        status = row.find_element(By.XPATH, f"td[{headlines.index('Status') + 1}]").text
        cpr = row.find_element(By.XPATH, f"td[{headlines.index('CPR-nr.') + 1}]/a").text
        name = row.find_element(By.XPATH, f"td[{headlines.index('Navn') + 1}]").text
        case_worker = row.find_element(By.XPATH, f"td[{headlines.index('Sagsbehandler') + 2}]").text  # eFlyt has an additional empty column before "Sagsbehandler"

        cases.append(Case(case_number, deadline, case_types, status, cpr, name, case_worker))

    return cases


def open_case(browser: webdriver.Chrome, case: str):
    """Open a case by searching for its case number.

    Args:
        browser: The webdriver browser object.
        case: The case to open.
    """
    # The id for both the search field and search button changes based on the current view hence the weird selectors.
    browser.get("https://notuskommunal.scandihealth.net/web/SearchResulteFlyt.aspx")
    case_input = browser.find_element(By.ID, 'ctl00_ContentPlaceHolder1_SearchControl_txtSagNr')
    case_input.clear()
    case_input.send_keys(case)

    browser.find_element(By.ID, 'ctl00_ContentPlaceHolder1_SearchControl_btnSearch').click()
