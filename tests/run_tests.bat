:: Change dir to parent dir
cd /d %~dp0..

:: Delete old venv
rmdir /s /q venv

:: Setup venv
python -m venv venv
call venv/Scripts/activate
pip install .

:: Run all unittests
python -m unittest discover

pause