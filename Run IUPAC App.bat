@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=%~dp0.venv\Scripts\python.exe"
if not exist "%PYTHON%" set "PYTHON=python"

echo Starting IUPAC Nomenclature...
start "" /b powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:5000'"
"%PYTHON%" "%~dp0iupac_app\app.py"

echo.
echo The server has stopped. You can close this window.
pause
