@echo off
REM Install.bat - Shipkit Installer
REM Double-click this file to install Shipkit

setlocal EnableDelayedExpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================================
    echo                          ERROR: PYTHON NOT FOUND
    echo ========================================================================
    echo.
    echo Python is required to install Shipkit.
    echo.
    echo Please install Python from: https://www.python.org/
    echo.
    echo After installing Python, run this installer again.
    echo.
    pause
    exit /b 1
)

REM Display header
cls
echo.
echo ========================================================================
echo                          SHIPKIT INSTALLER
echo ========================================================================
echo.
echo   Complete Product Development Framework
echo   Claude Code Skills + Agents + Workflows
echo.
echo ========================================================================
echo.

REM ============================================================================
REM STEP 1: Select Edition
REM ============================================================================
echo [STEP 1/2] Select Edition
echo.
echo   [1] Lite      - Fast, minimal (17 skills, POCs and side projects)
echo   [2] Default   - Complete (24 skills, full product development)
echo.
set /p EDITION_CHOICE="Select edition [1-2]: "

if "%EDITION_CHOICE%"=="1" (
    set "PROFILE=lite"
    echo.
    echo Selected: Lite Edition
) else if "%EDITION_CHOICE%"=="2" (
    set "PROFILE=default"
    echo.
    echo Selected: Default Edition
) else (
    echo.
    echo Invalid choice. Defaulting to Lite Edition.
    set "PROFILE=lite"
)

echo.
pause

REM ============================================================================
REM STEP 2: Select Scripting Language
REM ============================================================================
cls
echo.
echo ========================================================================
echo                          SHIPKIT INSTALLER
echo ========================================================================
echo.
echo   Edition: %PROFILE%
echo.
echo ========================================================================
echo.
echo [STEP 2/2] Select Scripting Language
echo.
echo   [1] Bash      - Traditional shell scripts (cross-platform)
echo   [2] Python    - Python scripts (recommended)
echo.
set /p LANGUAGE_CHOICE="Select language [1-2]: "

if "%LANGUAGE_CHOICE%"=="1" (
    set "LANGUAGE=bash"
    echo.
    echo Selected: Bash
) else if "%LANGUAGE_CHOICE%"=="2" (
    set "LANGUAGE=python"
    echo.
    echo Selected: Python
) else (
    echo.
    echo Invalid choice. Defaulting to Python.
    set "LANGUAGE=python"
)

echo.
echo Starting installation...
echo.

REM ============================================================================
REM Launch Python installer
REM ============================================================================

python "%SCRIPT_DIR%install.py" --profile=%PROFILE% --language=%LANGUAGE%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Installation failed with error code %ERRORLEVEL%
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Installation completed successfully!
echo.
pause

endlocal
