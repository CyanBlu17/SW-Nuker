@echo off
REM Ensure Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo requirements.txt not found.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

REM Clear the terminal screen
cls

REM Run the nuker
echo Starting the nuker...
python main.py
if %errorlevel% neq 0 (
    echo Failed to run the nuker.
    pause
    exit /b 1
)

pause
