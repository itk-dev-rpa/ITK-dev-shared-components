from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


@dataclass
class Case:
    """A dataclass representing an Eflyt case."""
    case_number: str
    deadline: str
    case_types: list[str]


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


def get_phone_numbers(browser: webdriver.Chrome) -> tuple[str, str]:
    """Extract the phone numbers associated with the case.

    Args:
        browser: The browser object.

    Returns:
        The persons phone and mobile numbers.
    """

    phone_number = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_stcPersonTab1_lblTlfnrTxt").text
    mobile_number = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_stcPersonTab1_lblMobilTxt").text

    return phone_number, mobile_number


def get_beboere(browser: webdriver.Chrome) -> list[WebElement]:
    """Count the number of beboere living on the address.

    Args:
        browser: The webdriver browser object.

    Returns:
        The number of beboere on the address.
    """
    change_tab(browser, 1)
    beboer_table = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_becPersonTab_GridViewBeboere")
    rows = beboer_table.find_elements(By.TAG_NAME, "tr")

    # Remove header
    rows.pop(0)

    return rows


def count_beboere(beboere: list[WebElement]) -> int:
    '''Return length of list'''
    return len(beboere)


def check_beboer(beboer_name: str, beboere: list[WebElement]):
    """Check if the given person is on the list of beboere.
    The names are stripped of any whitespace to give a more precise result.

    Args:
        browser: The webdriver browser object.
        beboer_name: The name to find in the beboer list.

    Returns:
        True if the beboer_name is on the list.
    """

    for row in beboere:
        name = row.find_element(By.XPATH, "td[3]").text
        if name.replace(" ", "") == beboer_name.replace(" ", ""):
            return True

    return False


def get_room_count(browser: webdriver.Chrome) -> int:
    """Get the number of rooms on the address.

    Args:
        browser: The webdriver browser object.

    Returns:
        The number of rooms on the address.
    """
    area_room_text = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_stcPersonTab6_lblAreaText").text
    room_text = area_room_text.split("/")[1]
    return int(room_text)


def get_applicants(browser: webdriver.Chrome) -> list[str]:
    """Get a list of applicants' cpr numbers from the applicant table.

    Args:
        browser: The webdriver browser object.

    Returns:
        A list of cpr numbers.
    """
    table = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_GridViewMovingPersons")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Remove header row
    rows.pop(0)

    cpr_list = []

    for row in rows:
        cpr = row.find_element(By.XPATH, "td[2]/a[2]").text
        cpr = cpr.replace("-", "")
        cpr_list.append(cpr)

    return cpr_list


def change_tab(browser: webdriver.Chrome, tab_index: int):
    """Change the tab in the case view e.g. 'Sagslog', 'Breve'.

    Args:
        browser: The webdriver browser object.
        tab_index: The zero-based index of the tab to select.
    """
    browser.execute_script(f"__doPostBack('ctl00$ContentPlaceHolder2$ptFanePerson$ImgJournalMap','{tab_index}')")


def create_note(browser: webdriver.Chrome, note_text: str):
    """Create a note on the case."""
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_ncPersonTab_ButtonVisOpdater").click()

    text_area = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_ncPersonTab_txtVisOpdaterNote")

    text_area.send_keys(note_text)
    text_area.send_keys("\n\n")

    browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_ncPersonTab_btnLongNoteUpdater").click()
