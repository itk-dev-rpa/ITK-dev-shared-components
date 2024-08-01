@echo off

:: Change dir to parent dir
echo Changing directory...
cd /d %~dp0..


choice /C YN /M "Do you want to reset venv?"

if errorlevel 2 (
    echo Activating excisting venv...
    call .venv-test\Scripts\activate

) else (
    echo Setting up new venv...
    python -m venv .venv-test
    call .venv-test\Scripts\activate

    echo Installing package...
    pip install .
    pip install .[dev]
)

echo Running unit tests...
python -m unittest discover

pause