import subprocess
def login_cli(username: str, password: str, client='751', system='P02') -> None:
    """
    Login SAP with commnd line arguments.
    :param username: AZ username
    :param password: password
    :param client: Kommune ID (Aarhus = 751)
    :param system: Environment SID (e.g. P02 = 'KMD OPUS Produktion [P02]')
    :return:
    """
    subprocess.run(["C:\Program Files (x86)\SAP\FrontEnd\SAPgui\sapshcut.exe",
                f"-system={system}",
                f"-client={client}",
                f"-user={username}",
                f"-pw={password}"
                ])

if __name__ == "__main__":
    login_cli('az12345', 'P4$$w0rd')
