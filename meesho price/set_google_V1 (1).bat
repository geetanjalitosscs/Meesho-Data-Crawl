@echo off

REM Set the default path to Google Chrome
set CHROME_PATH=%ProgramFiles%\Google\Chrome\Application\chrome.exe

REM Set the path to the existing Chrome user data directory
set USER_DATA_DIR=%LOCALAPPDATA%\Google\Chrome\User Data\Profile 2

REM Check if Chrome is installed in the default location
if exist "%CHROME_PATH%" (
    echo Starting Chrome with remote debugging using existing profile...
    "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%USER_DATA_DIR%"
) else (
    echo Google Chrome not found in the default location: %CHROME_PATH%
    echo Please install Google Chrome or modify this script to point to the correct location.
)

pause
