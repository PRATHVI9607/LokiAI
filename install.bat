@echo off
setlocal EnableDelayedExpansion

echo ============================================================
echo   LOKI AI Desktop Assistant — Installer
echo ============================================================
echo.

:: Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.10+ from python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% found

:: Check Python >= 3.10
python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.10 or higher required. Found %PYVER%
    pause
    exit /b 1
)

:: Create virtual environment
if not exist venv (
    echo.
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

:: Activate venv
call venv\Scripts\activate.bat

:: Upgrade pip
echo.
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip --quiet

:: Install PyTorch (CPU version is ~700MB smaller — change to cu121 for CUDA)
echo.
echo [3/4] Installing PyTorch ^(CPU^)...
echo       ^(This may take several minutes on first install^)
pip install torch --index-url https://download.pytorch.org/whl/cpu --quiet
if errorlevel 1 (
    echo [WARN] PyTorch install failed — trying default index...
    pip install torch --quiet
)

:: Install remaining requirements
echo.
echo [4/4] Installing Loki requirements...
pip install -r loki\requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Dependency installation failed. Check errors above.
    pause
    exit /b 1
)

:: Set up .env
if not exist loki\.env (
    echo.
    echo [SETUP] Creating loki\.env from template...
    copy loki\.env.example loki\.env >nul
    echo.
    echo ============================================================
    echo   ACTION REQUIRED:
    echo   Edit loki\.env and add your OPENROUTER_API_KEY
    echo   Get a free key at: https://openrouter.ai/keys
    echo ============================================================
) else (
    echo [OK] loki\.env already exists
)

echo.
echo ============================================================
echo   Installation complete!
echo   Run Loki with:  run.bat
echo   Or manually:    venv\Scripts\activate ^& python main.py
echo ============================================================
echo.
pause
