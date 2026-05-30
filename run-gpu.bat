@echo off
REM ════════════════════════════════════════════════════════════════════
REM  Loki — GPU launcher (self-bootstrapping via uv + Python 3.12 + CUDA)
REM  First run installs everything; later runs start instantly.
REM ════════════════════════════════════════════════════════════════════
cd /d %~dp0
setlocal

set "PY=.venv-gpu\Scripts\python.exe"
set "TORCH_SENTINEL=.venv-gpu\.torch-cu121-ok"

REM 0. uv present?
where uv >nul 2>&1
if errorlevel 1 (
  echo [setup] 'uv' is not installed. Install it first:
  echo         powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 ^| iex"
  exit /b 1
)

REM 1. create the Python 3.12 venv if missing
if not exist "%PY%" (
  echo [setup] Creating Python 3.12 GPU environment with uv...
  uv venv --python 3.12 .venv-gpu || goto :fail
)

REM 2. install CUDA torch once (the big one) — skip if already done
if not exist "%TORCH_SENTINEL%" (
  echo [setup] Installing CUDA PyTorch ^(~2.5GB, first time only^)...
  uv pip install --python "%PY%" torch --index-url https://download.pytorch.org/whl/cu121 || goto :fail
  echo ok> "%TORCH_SENTINEL%"
)

REM 3. sync all other deps every run (fast no-op; catches newly added packages)
echo [setup] Syncing dependencies...
uv pip install --python "%PY%" -r loki\requirements.txt || goto :fail

REM 4. launch
echo [run] Starting Loki on the GPU...
"%PY%" main.py %*
goto :eof

:fail
echo.
echo [setup] FAILED. See the errors above.
exit /b 1
