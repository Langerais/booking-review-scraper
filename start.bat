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

:: Install all requirements
echo [*] Installing dependencies...
%PYTHON% -m pip install --no-cache-dir -r requirements.txt

:: Run the main CLI menu
echo [*] Launching Booking Review Assistant...
%PYTHON% menu.py

endlocal
pause
