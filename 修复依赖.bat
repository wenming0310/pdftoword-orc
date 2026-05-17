@echo off
chcp 65001 >nul
echo ========================================
echo   PDF转Word转换器 - 依赖修复工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo [信息] 正在检查和修复依赖...
echo.

REM 升级pip
echo [1/4] 升级pip...
python -m pip install --upgrade pip
echo.

REM 重新安装PyQt5
echo [2/4] 重新安装PyQt5和PyQt5-tools...
pip uninstall PyQt5 PyQt5-tools -y
pip install PyQt5 PyQt5-tools
echo.

REM 安装其他依赖
echo [3/4] 安装其他依赖...
pip install -r requirements.txt
echo.

REM 验证安装
echo [4/4] 验证安装...
python -c "import PyQt5; print('[成功] PyQt5 版本:', PyQt5.QtCore.PYQT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo [警告] PyQt5 安装可能有问题
) else (
    echo [成功] PyQt5 安装正常
)
echo.

echo ========================================
echo   依赖修复完成！
echo ========================================
echo.
echo 现在你可以：
echo 1. 双击 启动程序.bat 运行程序
echo 2. 或者运行: python pdf_to_word_gui.py
echo.
echo 如果还有问题，运行 诊断.bat 进行检查
echo.
pause
