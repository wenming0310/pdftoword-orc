@echo off
chcp 65001 >nul
color 0B

:menu
cls
echo ==============================================================
echo         PDF转Word转换器 - 诊断和启动工具
echo ==============================================================
echo.
echo   请选择操作：
echo.
echo   [1] 运行完整诊断（推荐首次运行）
echo   [2] 测试Tesseract OCR配置
echo   [3] 测试PDF转换功能
echo   [4] 启动主程序
echo   [5] 全部运行
echo.
echo   [0] 退出
echo.
echo ==============================================================
echo.

set /p choice=请输入选项 [0-5]: 

if "%choice%"=="1" goto diagnose
if "%choice%"=="2" goto test_tesseract
if "%choice%"=="3" goto test_conversion
if "%choice%"=="4" goto start_program
if "%choice%"=="5" goto all_tests
if "%choice%"=="0" goto end

echo 无效选项，请重新选择
timeout /t 2 >nul
goto menu

:diagnose
cls
echo ==============================================================
echo                    运行完整诊断
echo ==============================================================
echo.
call :activate_venv
python diagnose_and_fix.py
echo.
pause
goto menu

:test_tesseract
cls
echo ==============================================================
echo                  测试Tesseract OCR
echo ==============================================================
echo.
call :activate_venv
python test_tesseract_simple.py
echo.
pause
goto menu

:test_conversion
cls
echo ==============================================================
echo                  测试PDF转换功能
echo ==============================================================
echo.
call :activate_venv
python test_conversion_cli.py
echo.
pause
goto menu

:start_program
cls
echo ==============================================================
echo                    启动主程序
echo ==============================================================
echo.
call :activate_venv
python pdf_to_word_gui.py
echo.
echo 程序已退出
pause
goto menu

:all_tests
cls
echo ==============================================================
echo                  运行所有测试
echo ==============================================================
echo.
call :activate_venv
echo [1/3] 运行完整诊断...
python diagnose_and_fix.py
echo.
timeout /t 3 >nul

echo [2/3] 测试Tesseract OCR...
python test_tesseract_simple.py
echo.
timeout /t 3 >nul

echo [3/3] 测试PDF转换功能...
python test_conversion_cli.py
echo.

echo ==============================================================
echo                  测试完成
echo ==============================================================
echo.
echo [提示] 是否启动主程序？
set /p start_now=请输入 Y 启动，或 N 返回菜单: 
if /i "%start_now%"=="Y" goto start_program
if /i "%start_now%"=="y" goto start_program
goto menu

:activate_venv
:: 尝试激活虚拟环境
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat >nul 2>&1
    goto :eof
)
:: 如果没有虚拟环境，直接返回
goto :eof

:end
cls
echo ==============================================================
echo                     再见！
echo ==============================================================
echo.
timeout /t 2 >nul
exit

