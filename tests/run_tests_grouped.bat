@echo off
setlocal enabledelayedexpansion

cd /d %~dp0..

if not exist .venv-test\Scripts\activate.bat (
    echo [ERROR] No venv at .venv-test. Run tests\run_tests.bat first to create it.
    exit /b 1
)

call .venv-test\Scripts\activate.bat

set GROUPS=test_misc test_smtp test_sap test_graph test_nova_api test_eflyt test_getorganized

set IDX=0
for %%G in (%GROUPS%) do (
    set /a IDX+=1
    set "GROUP_!IDX!=%%G"
    echo.
    echo ============================================================
    echo Running tests\%%G
    echo ============================================================
    python -m unittest discover -s tests\%%G -t .
    if errorlevel 1 (
        set "STATUS_!IDX!=FAIL"
    ) else (
        set "STATUS_!IDX!=PASS"
    )
)

echo.
echo ============================================================
echo Summary
echo ============================================================
for /L %%I in (1,1,!IDX!) do (
    echo   !GROUP_%%I! : !STATUS_%%I!
)
echo.

pause
