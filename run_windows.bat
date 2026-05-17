@echo off
chcp 65001 >nul
echo ========================================
echo   启动PDF转Word转换器
echo ========================================
echo.

:: 激活虚拟环境（如果存在）
if exist venv\Scripts\activate.bat (
    echo [提示] 激活虚拟环境...
    call venv\Scripts\activate.bat
    echo.
)

:: 运行主程序
echo [启动] 正在启动程序...
python pdf_to_word_gui.py

:: 如果程序退出，显示提示
echo.
echo ========================================
echo   程序已退出
echo ========================================
pause

