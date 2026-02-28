@echo off
chcp 65001 >nul
echo ========================================
echo   Finance Dashboard - 启动脚本
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [检查] Python 已安装
echo.

REM 检查依赖
echo [检查] 检查依赖...
python -c "import eel" >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [完成] 依赖检查通过
echo.

REM 启动应用
echo [启动] 正在启动 Finance Dashboard...
echo.
python backend/main.py

pause
