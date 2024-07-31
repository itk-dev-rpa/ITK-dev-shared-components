"""Tests relating to the module misc.file_util."""

import unittest
import os
import time
import threading
import shutil
import subprocess

from itk_dev_shared_components.misc import file_util
import uiautomation


class TestFileUtil(unittest.TestCase):
    """Tests relating to the module misc.file_util."""

    def test_wait_for_download(self):
        """Test the function wait_for_download."""
        download_folder = "test_downloads"
        if os.path.exists(download_folder):
            shutil.rmtree(download_folder)
        os.makedirs(download_folder)

        # Test timeout
        with self.assertRaises(TimeoutError):
            file_util.wait_for_download(download_folder, "foo", ".bar", 1)

        # Test with name
        file_name = "test.txt"
        name, ext = os.path.splitext(file_name)
        self._write_file_with_delay(download_folder, file_name, 1)
        path = file_util.wait_for_download(download_folder, name, ext)
        self.assertEqual(path, os.path.join(download_folder, file_name))

        # Test without name
        file_name = "test2.csv"
        name, ext = os.path.splitext(file_name)
        self._write_file_with_delay(download_folder, file_name, 1)
        path = file_util.wait_for_download(download_folder, None, ext)
        self.assertEqual(path, os.path.join(download_folder, file_name))

        shutil.rmtree(download_folder)

    def _write_file_with_delay(self, folder_path, file_name, delay: float):
        """A helper function that writes a file after
        a delay in a new thread.

        Args:
            folder_path: The folder to write the file to.
            file_name: The name of the file to write.
            delay: The time in seconds to wait before writing.
        """
        def delayed_write():
            time.sleep(delay)
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'w', encoding="utf8") as file:
                file.write("Test")

        thread = threading.Thread(target=delayed_write)
        thread.start()

    def test_handle_save_dialog(self):
        folder = os.path.join(os.getcwd(), "test_folder")
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

        # Open notepad and save file to open save dialog
        subprocess.Popen('notepad.exe', shell=True)
        notepad = uiautomation.WindowControl(searchDepth=1, ClassName='Notepad')
        notepad.SendKeys("{ctrl}s")

        file_path = os.path.join(folder, "test.txt")
        file_util.handle_save_dialog(file_path)

        self.assertTrue(os.path.exists(file_path))

        shutil.rmtree(folder)
        os.system("taskkill /F /IM notepad.exe > NUL 2>&1")


if __name__ == '__main__':
    unittest.main()
