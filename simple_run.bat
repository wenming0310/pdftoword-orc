@echo off
chcp 65001 >nul
title PDF转Word转换器 - 诊断工具

echo ==============================================================
echo         PDF转Word转换器 - 诊断和启动工具
echo ==============================================================
echo.
echo 正在检查环境...
echo.

:: 检查Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python！
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

:: 激活虚拟环境（如果存在）
if exist "venv\Scripts\activate.bat" (
    echo [提示] 激活虚拟环境...
    call "venv\Scripts\activate.bat"
) else (
    echo [提示] 未找到虚拟环境，使用系统Python
)

:: 创建临时脚本文件
echo.
echo [1/4] 创建诊断脚本...
(
echo import sys
echo import os
echo 
echo def check_all():
echo     print("=" * 60)
echo     print("PDF转Word转换器 - 环境诊断")
echo     print("=" * 60)
echo.
echo     # Python版本
echo     print(f"Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
echo.
echo     # 检查模块
echo     modules = ["PyQt5", "fitz", "pdf2docx", "pytesseract", "PIL", "docx", "cv2", "numpy"]
echo     for mod in modules:
echo         try:
echo             __import__(mod)
echo             print(f"✓ {mod}")
echo         except:
echo             print(f"✗ {mod} 未安装")
echo.
echo     # 检查Tesseract
echo     print()
echo     print("检查Tesseract OCR...")
echo     try:
echo         import pytesseract
echo         print(f"配置路径: {pytesseract.pytesseract.tesseract_cmd}")
echo         if os.path.exists(pytesseract.pytesseract.tesseract_cmd):
echo             print("✓ Tesseract可执行文件存在")
echo         else:
echo             print("✗ Tesseract路径不存在")
echo     except Exception as e:
echo         print(f"✗ 错误: {e}")
echo.
echo     # 检查主程序
echo     print()
echo     print("检查主程序...")
echo     try:
echo         import pdf_to_word_gui
echo         print("✓ 主程序导入成功")
echo     except Exception as e:
echo         print(f"✗ 导入失败: {e}")
echo.
echo if __name__ == "__main__":
echo     check_all()
echo     input("\n按Enter键退出...")
) > temp_diagnose.py

echo.
echo [2/4] 运行诊断...
python temp_diagnose.py

echo.
echo [3/4] 清理临时文件...
if exist temp_diagnose.py del temp_diagnose.py
if exist temp_diagnose.pyc del temp_diagnose.pyc

echo.
echo [4/4] 准备启动程序...
echo.
echo ==============================================================
echo                    启动主程序
echo ==============================================================
echo.
echo [提示] 如果程序无法启动，请将错误信息发送给我
echo.

:: 启动主程序
python pdf_to_word_gui.py

:: 如果程序退出
echo.
echo ==============================================================
echo                    程序已退出
echo ==============================================================
echo.
pause

