@echo off
chcp 65001 >nul
title PDF转Word转换器

echo ==============================================================
echo          PDF转Word转换器 - 诊断和启动工具
echo ==============================================================
echo.

:: 检查Python是否安装
python --version 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到Python！
    echo 请先安装Python 3.7或更高版本
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit
)

echo [OK] Python已安装
python --version
echo.

:: 检查虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo [提示] 找到虚拟环境，正在激活...
    call venv\Scripts\activate.bat
    echo.
) else (
    echo [提示] 未找到虚拟环境，使用系统Python
    echo.
)

:: 运行诊断
echo ==============================================================
echo                    环境诊断
echo ==============================================================
echo.
python -c "import sys; print(f'Python版本: {sys.version}')"
echo.

echo 检查必需模块...
python -c "import PyQt5; print('[OK] PyQt5')" 2>nul || echo "[FAIL] PyQt5"
python -c "import fitz; print('[OK] fitz/PyMuPDF')" 2>nul || echo "[FAIL] fitz"
python -c "import pdf2docx; print('[OK] pdf2docx')" 2>nul || echo "[FAIL] pdf2docx"
python -c "import pytesseract; print('[OK] pytesseract')" 2>nul || echo "[FAIL] pytesseract"
python -c "import PIL; print('[OK] PIL/Pillow')" 2>nul || echo "[FAIL] PIL"
python -c "import docx; print('[OK] docx')" 2>nul || echo "[FAIL] docx"
python -c "import cv2; print('[OK] opencv')" 2>nul || echo "[FAIL] opencv"
python -c "import numpy; print('[OK] numpy')" 2>nul || echo "[FAIL] numpy"
echo.

:: 检查Tesseract
echo ==============================================================
echo              检查Tesseract OCR
echo ==============================================================
echo.
if exist "D:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [OK] Tesseract已安装: D:\Program Files\Tesseract-OCR\tesseract.exe
) else (
    echo [FAIL] Tesseract未找到！
    echo 请下载并安装Tesseract OCR
    echo 下载地址：https://github.com/UB-Mannheim/tesseract/wiki
)
echo.

:: 检查主程序
echo ==============================================================
echo              检查主程序文件
echo ==============================================================
echo.
if exist "pdf_to_word_gui.py" (
    echo [OK] 主程序文件存在: pdf_to_word_gui.py
) else (
    echo [FAIL] 主程序文件不存在！
    echo 请确保 pdf_to_word_gui.py 在当前目录
)
echo.

:: 测试导入
echo ==============================================================
echo              测试程序导入
echo ==============================================================
echo.
python -c "import pdf_to_word_gui; print('[OK] 主程序模块导入成功')" 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] 主程序导入失败
    echo 可能是依赖库未安装或版本不兼容
)
echo.

echo ==============================================================
echo              准备启动程序
echo ==============================================================
echo.
echo [提示] 即将启动PDF转Word转换器
echo [提示] 如果程序无法启动，请将错误信息发送给我
echo.
pause

:: 启动程序
python pdf_to_word_gui.py

echo.
echo ==============================================================
echo              程序已退出
echo ==============================================================
pause

