"""Preflight check for required env vars and external services."""

import os
import shutil
import socket
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

REQUIRED_ENV = {
    "SAP_LOGIN": "test_sap/*",
    "GRAPH_API": "test_graph/test_mail.py",
    "MAIL_USER": "test_graph/test_mail.py",
    "MAIL_FOLDER_PREFIX": "test_graph/test_mail.py",
    "MAIL_FOLDER_COUNT": "test_graph/test_mail.py",
    "MAIL_FOLDER1": "test_graph/test_mail.py",
    "MAIL_FOLDER2": "test_graph/test_mail.py",
    "NOVA_CREDENTIALS": "test_nova_api/*",
    "NOVA_PARTY": "test_nova_api/test_cases.py",
    "NOVA_DEPARTMENT": "test_nova_api/test_cases.py",
    "NOVA_USER": "test_nova_api/*",
    "NOVA_USER_GROUP": "test_nova_api/test_cases.py, test_tasks.py",
    "NOVA_CPR_CASE": "test_nova_api/test_cases.py",
    "NOVA_CVR_CASE": "test_nova_api/test_cases.py",
    "NOVA_GROUP_CASE": "test_nova_api/test_cases.py",
    "CVR_CREDS": "test_misc/test_cvr_lookup.py",
    "EFLYT_LOGIN": "test_eflyt/*",
    "TEST_CASE": "test_eflyt/test_case.py, test_search.py",
    "TEST_CASE_NOONE": "test_eflyt/test_case.py",
    "TEST_CPR": "test_eflyt/test_case.py",
    "GO_LOGIN": "test_getorganized/test_case.py",
    "GO_APIURL": "test_getorganized/test_case.py",
    "GO_CATEGORY": "test_getorganized/test_case.py",
    "GO_DEPARTMENT": "test_getorganized/test_case.py",
    "GO_KLE": "test_getorganized/test_case.py",
}

OPTIONAL_ENV = {
    "SAP_NEW_PASSWORD": "test_sap_login.py (password-change subtest)",
    "mailpit_host": "test_smtp (default: localhost)",
    "mailpit_smtp_port": "test_smtp (default: 1025)",
    "mailpit_http_port": "test_smtp (default: 8025)",
}


def line(ok, label, detail=""):
    tag = "[OK]      " if ok else "[MISSING] "
    print(f"{tag}{label}" + (f"  -- {detail}" if detail else ""))


def check_env():
    print("\n--- Required env vars ---")
    missing = []
    for key, used_by in REQUIRED_ENV.items():
        ok = bool(os.environ.get(key))
        line(ok, key, used_by if not ok else "")
        if not ok:
            missing.append(key)

    print("\n--- Optional env vars ---")
    for key, used_by in OPTIONAL_ENV.items():
        is_set = bool(os.environ.get(key))
        tag = "[set]     " if is_set else "[unset]   "
        print(f"{tag}{key}  -- {used_by}")
    return missing


def tcp_check(host, port, timeout=2.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def check_mailpit():
    print("\n--- Mailpit (test_smtp) ---")
    host = os.environ.get("mailpit_host", "localhost")
    smtp_port = int(os.environ.get("mailpit_smtp_port", "1025"))
    http_port = int(os.environ.get("mailpit_http_port", "8025"))
    smtp_ok = tcp_check(host, smtp_port)
    http_ok = tcp_check(host, http_port)
    line(smtp_ok, f"Mailpit SMTP {host}:{smtp_port}")
    line(http_ok, f"Mailpit HTTP {host}:{http_port}")
    return smtp_ok and http_ok


def check_browser_drivers():
    print("\n--- Selenium drivers (test_eflyt) ---")
    found_any = False
    for driver in ("chromedriver", "msedgedriver", "geckodriver"):
        path = shutil.which(driver)
        line(bool(path), driver, path or "not in PATH")
        found_any = found_any or bool(path)
    return found_any


def check_sap_gui():
    print("\n--- SAP GUI (test_sap) ---")
    candidates = [
        r"C:\Program Files (x86)\SAP\FrontEnd\SAPGUI\sapshcut.exe",
        r"C:\Program Files\SAP\FrontEnd\SAPGUI\sapshcut.exe",
    ]
    found = shutil.which("sapshcut") or next((p for p in candidates if Path(p).is_file()), None)
    line(bool(found), "sapshcut.exe", found or "not in PATH nor default install dirs")
    return bool(found)


def main():
    print("=" * 60)
    print("ITK-dev-shared-components preflight check")
    print(f"Repo root: {REPO_ROOT}")
    print("=" * 60)

    missing_env = check_env()
    mailpit_ok = check_mailpit()
    drivers_ok = check_browser_drivers()
    sap_ok = check_sap_gui()

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    if missing_env:
        print(f"Missing env vars ({len(missing_env)}): {', '.join(missing_env)}")
    else:
        print("All required env vars set.")
    print(f"Mailpit:        {'OK' if mailpit_ok else 'NOT REACHABLE'}")
    print(f"Browser driver: {'OK' if drivers_ok else 'NONE FOUND'}")
    print(f"SAP GUI:        {'OK' if sap_ok else 'NOT FOUND'}")

    sys.exit(0 if not missing_env else 1)


if __name__ == "__main__":
    main()
