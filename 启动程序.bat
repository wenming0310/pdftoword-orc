@echo off
setlocal

echo ==============================================================
echo        PDF转Word转换器 - 启动工具
echo ==============================================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Python...
python --version
if errorlevel 1 (
    echo [错误] Python未安装或未配置PATH
    echo 请先安装Python
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖...
python -c "import sys; print('Python:', sys.version)" 
if errorlevel 1 goto :python_error

echo.
echo [3/3] 启动程序...
python pdf_to_word_gui.py
goto :end

:python_error
echo.
echo [错误] Python导入失败
echo 可能是依赖库未安装
echo 请运行: pip install -r requirements.txt
pause
exit /b 1

:end
echo.
echo ==============================================================
echo             程序已退出
echo ==============================================================
pause
