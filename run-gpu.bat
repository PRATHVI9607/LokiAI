@echo off
REM ── Run Loki on the GPU (Python 3.12 + CUDA torch in .venv-gpu) ──
REM Whisper transcription uses the RTX GPU. Much faster than CPU.
cd /d %~dp0
".venv-gpu\Scripts\python.exe" main.py %*
