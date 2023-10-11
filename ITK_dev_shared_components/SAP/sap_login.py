"""This module provides functions to handle opening and closing SAP Gui
as well as a function to change user passwords."""

import os
import pathlib
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pywintypes
import win32com.client
from ITK_dev_shared_components.SAP import multi_session


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
    _wait_for_sap_session(10)


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


def login_using_cli(username: str, password: str, client:str='751', system:str='P02', timeout:int=10) -> None:
    """Open and login to SAP with commandline expressions.

    Args:
        username: AZ username
        password: password
        client: Kommune ID (Aarhus = 751). Defaults to '751'.
        system: Environment SID (e.g. P02 = 'KMD OPUS Produktion [P02]'). Defaults to 'P02'.
        timeout: The time in seconds to wait for SAP Logon to start. Defaults to 10.

    Raises:
        TimeoutError: If SAP doesn't start within timeout limit.
        ValueError: If SAP is unable to log in using the given credentials.
    """

    command_args = [
        r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\sapshcut.exe",
        f"-system={system}",
        f"-client={client}",
        f"-user={username}",
        f"-pw={password}"
    ]

    subprocess.run(command_args, check=False)
    _wait_for_sap_session(timeout)
    if not _check_for_splash_screen():
        raise ValueError("Unable to log in. Please check username and password.")


def _wait_for_sap_session(timeout:int) -> None:
    """Check every second if the SAP Gui scripting engine is available until timeout is reached.

    Args:
        timeout: The time in seconds to wait for SAP Logon to start. Defaults to 10.

    Raises:
        TimeoutError: If SAP doesn't start within timeout limit.
    """
    for _ in range(timeout):
        time.sleep(1)
        try:
            sessions = multi_session.get_all_SAP_sessions()
            if len(sessions) > 0:
                return
        except pywintypes.com_error:
            pass

    raise TimeoutError(f"SAP didn't respond within timeout limit: {timeout} seconds.")

def _check_for_splash_screen() -> bool:
    """Check if the splash screen image is currently present.

    Returns:
        bool: True if the splash screen image is currently present.
    """
    session = multi_session.get_all_SAP_sessions()[0]
    image = session.findById("wnd[0]/usr/cntlIMAGE_CONTAINER/shellcont/shell/shellcont[1]/shell", False)

    return image is not None

def change_password(username:str, old_password:str, new_password:str,
                    client:str='751',
                    system:str='...KMD OPUS Produktion [P02]',
                    timeout:int=10) -> None:
    """Change the password of a user in SAP Gui. Closes SAP when done.

    Args:
        username: The username of the user.
        old_password: The current password of the user.
        new_password: The new password to change to.
        client: The client number. Defaults to '751'.
        system: The description string of the connection as displayed in SAP Logon. Defaults to '...KMD OPUS Produktion [P02]'.
        timeout: The time in seconds to wait for SAP Logon to start. Defaults to 10.

    Raises:
        TimeoutError: If the connection couldn't be established within the timeout limit.
        ValueError: If the current credentials are not valid or if the password can't be changed.
        ValueError: If the new password is not valid.
    
    """

    subprocess.Popen(r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe") #pylint: disable=consider-using-with

    # Wait for SAP Logon to open
    for _ in range(timeout):
        time.sleep(1)
        try:
            sap = win32com.client.GetObject("SAPGUI")
            app = sap.GetScriptingEngine
            app.OpenConnection(system)
            break
        except pywintypes.com_error:
            pass
    else:
        raise TimeoutError(f"SAP Logon didn't open within timeout limit: {timeout} seconds.")

    session = multi_session.get_all_SAP_sessions()[0]

    # Enter credentials
    session.findById("wnd[0]/usr/txtRSYST-MANDT").text = client
    session.findById("wnd[0]/usr/txtRSYST-BNAME").text = username
    session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = old_password
    session.findById("wnd[0]/tbar[1]/btn[5]").press()

    # Check status bar
    status_bar = session.findById("wnd[0]/sbar")
    if status_bar.MessageType != 'S':
        text = status_bar.Text
        kill_sap()
        raise ValueError(f"Password change was blocked: {text}")

    # Enter new password
    session.findById("wnd[1]/usr/pwdRSYST-NCODE").text = new_password
    session.findById("wnd[1]/usr/pwdRSYST-NCOD2").text = new_password
    session.findById("wnd[1]/tbar[0]/btn[0]").press()

    if not _check_for_splash_screen():
        kill_sap()
        raise ValueError("New password couldn't be set. Please check password requirements.")

    kill_sap()


def kill_sap():
    """Kills all SAP processes currently running."""
    os.system("taskkill /F /IM saplogon.exe > NUL 2>&1")
