"""This module contains functions for sending letters from a case in eFlyt."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from itk_dev_shared_components.eflyt import eflyt_case


def send_letter_to_anmelder(browser: webdriver.Chrome, letter_text: str) -> bool:
    """Open the 'Breve' tab and send a letter to the anmelder using the 'Individuelt brev'-template.

    Args:
        browser: The webdriver browser object.
        original_letter: The title of the original logiværtserklæring.

    Returns:
        bool: True if the letter was sent.
    """
    eflyt_case.change_tab(browser, tab_index=3)

    click_letter_template(browser, "- Individuelt brev")

    # Select the anmelder as the receiver
    select_letter_receiver(browser, "anmelder")

    # Click 'Send brev'
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_bcPersonTab_btnSendBrev").click()

    # Insert the correct letter text
    text_area = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_bcPersonTab_txtStandardText")
    text_area.clear()
    text_area.send_keys(letter_text)
    # Click 'Ok'
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_bcPersonTab_btnOK").click()

    # Check if a warning appears
    if check_digital_post_warning(browser):
        # Click 'Nej'
        browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_bcPersonTab_btnDeleteLetter").click()
        return False

    # Click 'Ja'
    browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_bcPersonTab_btnSaveLetter").click()
    return True


def click_letter_template(browser: webdriver.Chrome, letter_name: str):
    """Click the letter template with the given name under the "Breve" tab.

    Args:
        browser: The webdriver browser object.
        letter_name: The literal name of the letter template to click.

    Raises:
        ValueError: If the letter wasn't found in the list.
    """
    letter_table = browser.find_element(By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_bcPersonTab_GridViewBreveNew")
    rows = letter_table.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        text = row.find_element(By.XPATH, "td[2]").text
        if text == letter_name:
            row.find_element(By.XPATH, "td[1]/input").click()
            return

    raise ValueError(f"Template with the name '{letter_name}' was not found.")


def select_letter_receiver(browser: webdriver.Chrome, receiver_name: str) -> None:
    """Select the receiver for the letter. The search is fuzzy so it's only checked
    if the options contains the receiver name.

    I some cases there's only one option for the receiver in which
    case there's a text label instead of a select element. In this
    case the predefined name is still checked against the desired receiver.

    Args:
        browser: The webdriver browser object.
        receiver_name: The name of the receiver to select.

    Raises:
        ValueError: If the given name isn't found in the select options.
        ValueError: If the given name doesn't match the static label.
    """
    # Check if there is a select for the receiver name
    try:
        # Wait for the dropdown to be present
        name_select_element = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_bcPersonTab_ddlModtager"))
        )
        name_select = Select(name_select_element)

        # Wait until the dropdown has more than one option
        WebDriverWait(browser, 2).until(lambda browser: len(name_select.options) > 1)

        for i, option in enumerate(name_select.options):
            if receiver_name in option.text:
                name_select.select_by_index(i)
                return

        raise ValueError(f"'{receiver_name}' wasn't found on the list of possible receivers.")

    except TimeoutException:
        pass  # Continue to the next check if the dropdown is not found

    # If there's simply a label for the receiver, check if the name matches
    try:
        name_label = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_ptFanePerson_bcPersonTab_lblModtagerName"))
        )
        if receiver_name not in name_label.text:
            raise ValueError(f"'{receiver_name}' didn't match the predefined receiver.")
    except TimeoutException as exc:
        raise ValueError("Receiver name label did not load in time.") from exc


def check_digital_post_warning(browser: webdriver.Chrome) -> bool:
    """Check if a red warning text has appeared warning that
    a letter must be sent manually.

    Args:
        browser: The webdriver browser object.

    Returns:
        bool: True if the warning has appeared.
    """
    warning_text = browser.find_elements(By.XPATH, "//font[@color='red']")
    return len(warning_text) != 0 and "Dokumentet skal sendes manuelt" in warning_text[0].text
