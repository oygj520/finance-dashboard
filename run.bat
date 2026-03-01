@echo off
chcp 65001
echo ========================================
echo   Finance Dashboard - Start
echo ========================================
echo.

cd /d "%~dp0"

echo [Start] Starting Finance Dashboard...
echo.

py backend\main.py

pause
