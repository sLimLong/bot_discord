@echo off
cd /d "%~dp0"

echo === Searching for Python 3.12 ===

REM Ищем Python 3.12 через py launcher
for /f "tokens=2 delims= " %%A in ('py -0p ^| find "3.12"') do (
    set PY312=%%A
)

REM Если не нашли — ошибка
if "%PY312%"=="" (
    echo [ERROR] Python 3.12 not found on your system.
    echo Install Python 3.12 from https://www.python.org/downloads/
    echo And be sure to check "Add Python to PATH".
    pause
    exit /b
)

echo Found Python 3.12 at: %PY312%
echo.

echo === Installing dependencies ===
"%PY312%" -m pip install -r requirements.txt

echo.
echo === Starting bot ===
"%PY312%" main_discord.py

echo.
pause
