@echo off
REM Quick start script for Windows

echo.
echo 🚩 CTF Platform - Quick Start (Windows)
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Copy .env if it doesn't exist
if not exist ".env" (
    copy .env.example .env
    echo Created .env file - update SECRET_KEY if needed
)

REM Initialize database
echo.
echo Initializing database...
python init.py

REM Start the server
echo.
echo 🚀 Starting CTF Platform...
echo Access at: http://localhost:5000
echo.
python app.py

pause
