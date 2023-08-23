import pythoncom
import win32com.client
import win32gui
import time
import threading
from typing import Callable

def run_with_session(session_index:int, func:Callable, args:tuple) -> None:
    """Run a function in a sepcific session based on the sessions index.
    This function is meant to be run inside a seperate thread.
    The function must take a session object as its first argument.
    Note that this function will not spawn the sessions before running,
    use spawn_sessions to do that.
    """

    pythoncom.CoInitialize()

    SAP = win32com.client.GetObject("SAPGUI")
    app = SAP.GetScriptingEngine
    connection = app.Connections(0)
    session = connection.Sessions(session_index)

    func(session, *args)

    pythoncom.CoUninitialize()

def run_batch(func:Callable, args:tuple[tuple], num_sessions=6) -> None:
    """Run a function in parallel sessions.
    The function will be run {num_sessions} times with args[i] as input.
    The function must take a session object as its first argument.
    Note that this function will not spawn the sessions before running,
    use spawn_sessions to do that.
    """

    threads = []
    for i in range(num_sessions):
        t = ExThread(target=run_with_session, args=(i, func, args[i]))
        threads.append(t)
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for t in threads:
        if t.error:
            raise t.error

def run_batches(func:Callable, args:tuple[tuple], num_sessions=6):
    """Run a function in parallel batches.
    This function runs the input function for each set of arguments in args.
    The function will be run in parallel batches of size {num_sessions}.
    The function must take a session object as its first argument.
    Note that this function will not spawn the sessions before running,
    use spawn_sessions to do that.
    """

    for b in range(0, len(args), num_sessions):
        batch = args[b:b+num_sessions]
        run_batch(func, args, len(batch))

def spawn_sessions(num_sessions=6) -> list:
    """A function to spawn multiple sessions of SAP.
    This function will attempt to spawn the desired number of sessions.
    If the current number of open sessions exceeds the desired number of sessions
    the already open sessions will not be closed to match the desired number.
    The number of sessions must be between 1 and 6.
    Returns a list of all open sessions.
    """
    SAP = win32com.client.GetObject("SAPGUI")
    app = SAP.GetScriptingEngine
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

    sessions = list(connection.Sessions)
    num_sessions = len(sessions)

    if num_sessions == 1:
        c = 1
    elif num_sessions <= 4:
        c = 2
    elif num_sessions <= 6:
        c = 3

    if num_sessions < 3:
        r = 1
    else:
        r = 2

    w, h = 1920//c, 1040//r

    for i, session in enumerate(sessions):
        window = session.findById("wnd[0]")
        window.Restore()
        hwnd = window.Handle
        x = i % c * w
        y = i // c * h
        win32gui.MoveWindow(hwnd, x, y, w, h, True)
    
    return sessions

class ExThread(threading.Thread):
    """A thread with a handle to get an exception raised inside the thread: ExThread.error"""
    def __init__(self, *args, **kwargs):
        super(ExThread, self).__init__(*args, **kwargs)
        self.error = None

    def run(self):
        try:
            self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.error = e


