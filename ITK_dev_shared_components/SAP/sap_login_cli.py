"""This module provides a single static function that opens and logs into SAP GUI
using commandline expressions."""

import subprocess

def login_cli(username: str, password: str, client='751', system='P02') -> None:
    """Login SAP with command line arguments.

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
    

if __name__ == "__main__":
    login_cli('az12345', 'P4$$w0rd')
