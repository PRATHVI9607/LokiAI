@echo off
if not exist venv\Scripts\activate.bat (
    echo [ERROR] Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo Starting Loki AI...
echo Open http://localhost:7777 in your browser.
python main.py %*
