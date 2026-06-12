@echo off
cd /d %~dp0..

if not exist .venv-test\Scripts\activate.bat (
    echo [ERROR] No venv at .venv-test. Run tests\run_tests.bat first to create it.
    exit /b 1
)

call .venv-test\Scripts\activate.bat
python tests\preflight.py
