@echo off
setlocal enabledelayedexpansion

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

:: Get the hook script name from the first argument
set "HOOK_SCRIPT=%~1"

:: If no argument, exit
if "%HOOK_SCRIPT%"=="" (
    echo {"error": "No hook script specified"}
    exit /b 1
)

:: Try Git Bash first, then WSL bash, then fall back to sh
where bash >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    bash "%SCRIPT_DIR%%HOOK_SCRIPT%"
    exit /b %ERRORLEVEL%
)

:: Try sh (Git for Windows includes this)
where sh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    sh "%SCRIPT_DIR%%HOOK_SCRIPT%"
    exit /b %ERRORLEVEL%
)

:: No shell found
echo {"error": "No bash or sh found. Install Git for Windows or WSL."}
exit /b 1
