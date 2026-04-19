@echo off
cd /d "%~dp0"

echo Установка зависимостей из requirements.txt...
pip install -r requirements.txt

echo Запуск Discord-бота...
python main_discord.py

echo.
pause
