@echo off
echo Starting AI Storyteller (Demo Mode)...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH. Please install Python first.
    pause
    exit /b 1
)

:: Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt

:: Start the Flask backend
echo Starting server...
python app.py

pause
