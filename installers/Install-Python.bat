@echo off
REM Install-Python.bat - Install Shipkit using Python
REM Double-click this file to run the Python installer

setlocal

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Display header
echo.
echo ═══════════════════════════════════════════════════════
echo   Shipkit Installer - Python Version
echo ═══════════════════════════════════════════════════════
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/
    echo Or use the Bash installer instead: install.sh
    echo.
    pause
    exit /b 1
)

echo Starting Python installer...
echo.

REM Run the Python installer
python "%SCRIPT_DIR%install.py"

REM Keep window open
echo.
pause

endlocal
