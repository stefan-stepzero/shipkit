@echo off
REM Install-PowerShell.bat - Install Shipkit using PowerShell
REM Double-click this file to run the PowerShell installer

setlocal

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Display header
echo.
echo ═══════════════════════════════════════════════════════
echo   Shipkit Installer - PowerShell Version
echo ═══════════════════════════════════════════════════════
echo.
echo Starting PowerShell installer...
echo.

REM Launch PowerShell with the installer script
REM -NoExit keeps the window open after installation
REM -ExecutionPolicy Bypass allows the script to run without changing system policy
REM -File runs the script file directly
powershell.exe -NoExit -ExecutionPolicy Bypass -File "%SCRIPT_DIR%install.ps1"

endlocal
