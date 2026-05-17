@echo off
chcp 65001 >nul
echo ========================================
echo   PDF转Word带界面程序 - Windows设置
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python！
    echo 请先安装Python 3.7或更高版本
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] 检测到Python版本：
python --version
echo.

:: 检查是否在虚拟环境中
if defined VIRTUAL_ENV (
    echo [OK] 虚拟环境已激活
) else (
    echo [提示] 未检测到虚拟环境，建议创建虚拟环境
)
echo.

:: 安装依赖
echo [步骤1] 检查并安装依赖库...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装PyQt5和其他依赖...
    pip install -r requirements.txt
) else (
    echo [OK] PyQt5已安装
)
echo.

:: 检查Git
echo [步骤2] 检查Git状态...
where git >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到Git
    echo [提示] Git功能需要安装Git才能使用
    echo [提示] 如需Git功能，请访问：https://git-scm.com/download/win
    echo [提示] 安装后请重启程序
) else (
    echo [OK] Git已安装
    git --version
)
echo.

:: 创建测试PDF（如果有的话）
if exist test_conversion_cli.py (
    echo [步骤3] 运行功能测试...
    echo [提示] 这将创建测试PDF并转换
    python test_conversion_cli.py
    echo.
)

echo ========================================
echo   设置检查完成！
echo ========================================
echo.
echo [下一步] 运行程序：
echo   python pdf_to_word_gui.py
echo.
echo [提示] 如果遇到问题，请查看WINDOWS_RUN_GUIDE.md
echo.
pause

