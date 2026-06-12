"""This module provides static function to handle multiple sessions of SAP.
Using this module you can spawn multiple sessions and automatically execute
a function in parallel on the sessions."""

import time
import threading
from typing import Callable
import math

import pythoncom
import win32com.client
import win32gui
import win32api


def run_with_session(session_index: int, func: Callable, args: tuple) -> None:
    """Run a function in a specific session based on the sessions index.
    This function is meant to be run inside a separate thread.
    The function must take a session object as its first argument.
    Note that this function will not spawn the sessions before running,
    use spawn_sessions to do that.
    """
    pythoncom.CoInitialize()

    sap = win32com.client.GetObject("SAPGUI")
    app = sap.GetScriptingEngine
    connection = app.Connections(0)
    session = connection.Sessions(session_index)

    func(session, *args)

    pythoncom.CoUninitialize()


def run_batch(func: Callable, args: tuple[tuple]) -> None:
    """Run a function in parallel sessions.
    A number of threads equal to the length of args will be spawned.
    The function must take a session object as its first argument.
    Note that this function will not spawn the sessions before running,
    use spawn_sessions to do that.

    Args:
        func: A callable function to run in the threads.
        args: A tuple of tuples containing arguments to be passed to func.

    Raises:
        Exception: Any exception raised in any of the threads.
    """

    threads = []
    for i, arg in enumerate(args):
        t = ExThread(target=run_with_session, args=(i, func, arg))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for t in threads:
        if t.error:
            raise t.error


def run_batches(func: Callable, args: tuple[tuple], num_sessions: int = 6) -> None:
    """Run a function in parallel batches.
    This function runs the input function for each set of arguments in args.
    The function will be run in parallel batches of size {num_sessions}.
    The function must take a session object as its first argument.
    Note that this function will not spawn the sessions before running,
    use spawn_sessions to do that.
    """

    for b in range(0, len(args), num_sessions):
        batch = args[b:b+num_sessions]
        run_batch(func, batch)


def spawn_sessions(num_sessions=6) -> list:
    """A function to spawn multiple sessions of SAP.
    This function will attempt to spawn the desired number of sessions.
    If the current number of already open sessions exceeds the desired number of sessions
    the already open sessions will not be closed to match the desired number.
    The number of sessions must be between 1 and 6.

    Args:
        num_sessions: The number of sessions desired. Defaults to 6.

    Raises:
        ValueError: If the number of sessions is not between 1 and 6.

    Returns:
        tuple: A tuple of all currently open sessions.
    """
    sap = win32com.client.GetObject("SAPGUI")
    app = sap.GetScriptingEngine
    connection = app.Connections(0)
    session = connection.Sessions(0)

    if num_sessions < 1:
        raise ValueError("Number of sessions cannot be less than 1")
    if num_sessions > 6:
        raise ValueError("Number of sessions cannot be more than 6")

    for _ in range(num_sessions - connection.Sessions.count):
        session.CreateSession()

    # Wait for the sessions to spawn
    while connection.Sessions.count < num_sessions:
        time.sleep(0.1)

    arrange_sessions()

    return tuple(connection.Sessions)


def get_all_sap_sessions() -> tuple:
    """Returns a tuple of all open SAP sessions (on connection index 0).

    Returns:
        tuple: A tuple of SAP GuiSession objects.
    """
    sap = win32com.client.GetObject("SAPGUI")
    app = sap.GetScriptingEngine
    connection = app.Connections(0)
    return tuple(connection.Sessions)


def arrange_sessions():
    """Take all toplevel windows of currently open SAP sessions
    and arrange them equally on the screen.
    """
    sessions = get_all_sap_sessions()
    num_sessions = len(sessions)

    # Calculate number of columns and rows
    c = math.ceil(math.sqrt(num_sessions))
    r = math.ceil(num_sessions / c)

    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    w = screen_width // c
    h = screen_height // r

    for i, session in enumerate(sessions):
        window = session.findById("wnd[0]")
        window.Restore()
        hwnd = window.Handle
        x = i % c * w
        y = i // c * h
        win32gui.MoveWindow(hwnd, x, y, w, h, True)


class ExThread(threading.Thread):
    """A thread with a handle to get an exception raised inside the thread: ExThread.error"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error = None

    def run(self):
        try:
            self._target(*self._args, **self._kwargs)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.error = e
