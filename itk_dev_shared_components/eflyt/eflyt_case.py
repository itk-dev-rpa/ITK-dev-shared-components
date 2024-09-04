"""Module for handling cases in eFlyt"""
from dataclasses import dataclass
from datetime import date, datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


@dataclass
class Case:
    """A dataclass representing an Eflyt case."""
    case_number: str
    deadline: date | None
    case_types: list[str]
    status: str
    cpr: str
    name: str
    case_worker: str


@dataclass
class Inhabitant:
    """A dataclass representing an inhabitant."""
    cpr: str
    name: str
    move_in_date: date
    relations: list[str]


@dataclass
class Applicant:
    """A dataclass representing an applicant."""
    cpr: str
    name: str


def get_beboere(browser: webdriver.Chrome) -> list[Inhabitant]:
    """Get a list of current inhabitants on the case currently open.

    Args:
        browser: The webdriver browser object.

    Returns:
        A list of Inhabitants.
    """
    # Go to the correct tab and scrape data
    change_tab(browser, 1)
    beboer_table = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_becPersonTab_GridViewBeboere")
    rows = beboer_table.find_elements(By.TAG_NAME, "tr")

    # Remove header
    rows.pop(0)

    inhabitants = []
    for inhabitant in rows:
        # Get date for moving in, CPR and name
        moving_in = datetime.strptime(inhabitant.find_element(By.XPATH, "td[1]/span | td[1]/a").text, "%d-%m-%Y").date()
        cpr = inhabitant.find_element(By.XPATH, "td[2]").text.replace("-", "")
        name = inhabitant.find_element(By.XPATH, "td[3]").text

        # Check for a list of relations
        relations = []
        elements = inhabitant.find_elements(By.XPATH, "td[4]/span")
        if elements:
            relations = elements[0].text.replace("<br>", ";").replace("\n", ";").split(";")

        # Create an Inhabitant and add to list
        new_inhabitant = Inhabitant(cpr, name, moving_in, relations)
        inhabitants.append(new_inhabitant)

    return inhabitants


def get_room_count(browser: webdriver.Chrome) -> int:
    """Get the number of rooms on the address.

    Args:
        browser: The webdriver browser object.

    Returns:
        The number of rooms on the address.
    """
    change_tab(browser, 1)
    area_room_text = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_stcPersonTab6_lblAreaText").text
    room_text = area_room_text.split("/")[1]
    return int(room_text)


def get_applicants(browser: webdriver.Chrome) -> list[Applicant]:
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

    applicants = []

    for row in rows:
        cpr = row.find_element(By.XPATH, "td[2]/a[2]").text.replace("-", "")
        name = row.find_element(By.XPATH, "td[3]/a").text
        applicant = Applicant(cpr, name)
        applicants.append(applicant)

    return applicants


def change_tab(browser: webdriver.Chrome, tab_index: int):
    """Change the tab in the case view e.g. 'Sagslog', 'Breve'.

    Args:
        browser: The webdriver browser object.
        tab_index: The zero-based index of the tab to select.
    """
    # Use the src of the tab image to determine if the tab needs to be changed
    tab_image = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_ImgJournalMap")
    image_src = tab_image.get_attribute("src")
    current_index = int(image_src[-5]) - 1

    if current_index != tab_index:
        browser.execute_script(f"__doPostBack('ctl00$ContentPlaceHolder2$ptFanePerson$ImgJournalMap','{tab_index}')")
