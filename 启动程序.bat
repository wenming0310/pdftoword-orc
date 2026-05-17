@echo off
chcp 65001 >nul
echo ========================================
echo   PDF转Word转换器 - 启动程序
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo [成功] Python已安装
python --version
echo.

REM 检查是否在正确目录
if not exist "pdf_to_word_gui.py" (
    echo [错误] 未找到 pdf_to_word_gui.py
    echo 请确保你在项目根目录下运行此脚本
    pause
    exit /b 1
)

echo [成功] 找到程序文件
echo.
echo 正在启动程序...
echo.

REM 运行程序
python pdf_to_word_gui.py

if errorlevel 1 (
    echo.
    echo [错误] 程序异常退出
    pause
)
