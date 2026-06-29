"""This module handles opening and closing KMD Boliglån."""

import subprocess
import time
import os

import uiautomation


def login(username: str, password: str):
    """Launch and login to KMD Boliglån."""
    subprocess.Popen(r"C:\Program Files (x86)\KMD\KMD.LW.Boliglaan\KMD.LW.KMDBoliglaan.Client.exe")  # pylint: disable=consider-using-with

    kmd_logon = uiautomation.WindowControl(AutomationId="MainLogonWindow", searchDepth=1)

    # Wait for logon window to load
    for _ in range(5):
        try:
            if len(kmd_logon.ComboBoxControl(AutomationId="UserPwComboBoxCics").GetSelectionPattern().GetSelection()) == 1:
                break
        except LookupError:
            pass
        time.sleep(1)

    kmd_logon.EditControl(AutomationId="UserPwTextBoxUserName").GetValuePattern().SetValue(username)
    kmd_logon.EditControl(AutomationId="UserPwPasswordBoxPassword").GetValuePattern().SetValue(password)
    kmd_logon.ButtonControl(AutomationId="UserPwLogonButton").GetInvokePattern().Invoke()

    boliglaan = uiautomation.WindowControl(Name="KMD Boliglån", searchDepth=1)
    if not boliglaan.Exists(maxSearchSeconds=30):
        raise RuntimeError("Boliglån didn't appear within 30 seconds")


def kill_boliglaan():
    """Kill KMD Logon and KMD Boliglån."""
    os.system("taskkill /f /im KMD.LW.KMDBoliglaan.Client.exe")
    os.system("taskkill /f /im KMD.YH.Security.Logon.Desktop.exe")
