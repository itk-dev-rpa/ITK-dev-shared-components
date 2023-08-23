"""This module provides a functions to open SAP GUI."""

import os
import pathlib
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def login_using_portal(username:str, password:str):
    """Open KMD Portal in Edge, login and start SAP GUI.

    Args:
        user: KMD Portal username.
        password: KMD Portal password.
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('https://portal.kmd.dk/irj/portal')
    driver.maximize_window()

    #Login
    user_field = driver.find_element(By.ID, 'logonuidfield')
    pass_field = driver.find_element(By.ID, 'logonpassfield')
    login_button = driver.find_element(By.ID, 'buttonLogon')

    user_field.clear()
    user_field.send_keys(username)

    pass_field.clear()
    pass_field.send_keys(password)

    login_button.click()

    #Opus
    mine_genveje = driver.find_element(By.CSS_SELECTOR, "div[title='Mine Genveje']")
    mine_genveje.click()

    #Wait for download and launch file
    _wait_for_download()

    driver.quit()

    #TODO: Wait for if SAP has opened


def _wait_for_download():
    """Private function that checks if the SAP.erp file has been downloaded.

    Raises:
        TimeoutError: If the file hasn't been downloaded within 5 seconds.
    """
    downloads_folder = str(pathlib.Path.home() / "Downloads")
    for _ in range(10):
        for file in os.listdir(downloads_folder):
            if file.endswith(".sap"):
                path = os.path.join(downloads_folder, file)
                os.startfile(path)
                return
            
        time.sleep(0.5)
    raise TimeoutError(f".SAP file not found in {downloads_folder}")


def login_using_cli(username: str, password: str, client='751', system='P02') -> None:
    """Open and login to SAP with commandline expressions.

    Args:
        username (str): AZ username
        password (str): password
        client (str, optional): Kommune ID (Aarhus = 751). Defaults to '751'.
        system (str, optional): Environment SID (e.g. P02 = 'KMD OPUS Produktion [P02]'). Defaults to 'P02'.
    """    
    
    command_args = [
        r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\sapshcut.exe",
        f"-system={system}",
        f"-client={client}",
        f"-user={username}",
        f"-pw={password}"
    ]

    subprocess.run(command_args, check=False)


if __name__=="__main__":
    user = "az12345"
    password = "Hunter2"
    login_using_portal(user, password)
    login_using_cli(user, password)


