@echo off
setlocal

:: Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

:: Set path to Python from venv
set PYTHON=venv\Scripts\python.exe

:: Upgrade pip
echo [*] Upgrading pip...
%PYTHON% -m pip install --upgrade pip

:: Install dependencies
echo [*] Installing dependencies...
%PYTHON% -m pip install --no-cache-dir -r requirements.txt

:: Launch GUI app
echo [*] Starting GUI...
%PYTHON% gui.py

endlocal
pause
