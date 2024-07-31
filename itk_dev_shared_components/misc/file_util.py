"""This module contains helper functions to do with handling files."""

import os
import time

import uiautomation


def wait_for_download(folder: str, file_name: str | None, file_extension: str, timeout: int = 10) -> str:
    """Wait for a file to appear in a folder.
    This checks the folder every second for the file.

    Args:
        folder: The absolute path of the folder to monitor.
        file_name: The name of the file if know else None
        file_extension: The file extension of the file with the dot.
        timeout: The number of seconds to wait for the file.

    Returns:
        The absolute path to the file.

    Raises:
        TimeoutError: If the file didn't appear withing the given timeout.
    """
    for _ in range(timeout):
        files = os.listdir(folder)
        for file in files:
            name, ext = os.path.splitext(file)

            if file_extension == ext and (file_name is None or file_name == name):
                return os.path.join(folder, file)

        time.sleep(1)

    raise TimeoutError(f"Downloaded file didn't appear within {timeout} seconds.")


def handle_save_dialog(file_path: str):
    """Save a file using the default Windows file dialog.
    The dialog is assumed to already be open.

    Args:
        file_path: The absolute path to save the file at.
    """
    file_dialog = uiautomation.WindowControl(Name="Gem som", searchDepth=2)
    file_dialog.PaneControl(AutomationId="BackgroundClear", searchDepth=4).EditControl(AutomationId="1001").GetValuePattern().SetValue(file_path)
    file_dialog.ButtonControl(Name="Gem", searchDepth=1).GetInvokePattern().Invoke()
