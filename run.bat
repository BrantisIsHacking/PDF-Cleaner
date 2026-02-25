@echo off
echo Starting PDF Text Cleaner...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your OpenAI API key.
    echo.
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Start the application
echo.
echo Starting the application...
echo Open your browser and go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server.
echo.
python app.py
