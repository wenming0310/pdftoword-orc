@echo off
echo ==============================================================
echo        PDF转Word转换器 - 诊断工具
echo ==============================================================
echo.

echo [步骤 1/6] 检查Python...
python --version
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    pause
    exit /b 1
)
echo [OK] Python正常
echo.

echo [步骤 2/6] 检查PyQt5...
python -c "import PyQt5" 2>nul
if errorlevel 1 (
    echo [错误] PyQt5未安装
    echo 运行: pip install PyQt5
    pause
    exit /b 1
)
echo [OK] PyQt5正常
echo.

echo [步骤 3/6] 检查PDF处理库...
python -c "import fitz; import pdf2docx" 2>nul
if errorlevel 1 (
    echo [错误] PDF处理库未安装
    echo 运行: pip install pymupdf pdf2docx
    pause
    exit /b 1
)
echo [OK] PDF处理库正常
echo.

echo [步骤 4/6] 检查OCR支持...
python -c "import pytesseract; from PIL import Image" 2>nul
if errorlevel 1 (
    echo [错误] pytesseract未安装
    echo 运行: pip install pytesseract
    pause
    exit /b 1
)
echo [OK] pytesseract正常
echo.

echo [步骤 5/6] 检查Tesseract路径...
if not exist "D:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [警告] Tesseract可执行文件不存在
    echo 期望路径: D:\Program Files\Tesseract-OCR\tesseract.exe
) else (
    echo [OK] Tesseract可执行文件存在
)
echo.

echo [步骤 6/6] 检查主程序...
if not exist "pdf_to_word_gui.py" (
    echo [错误] 主程序文件不存在
    pause
    exit /b 1
)
echo [OK] 主程序文件存在
echo.

echo ==============================================================
echo                  环境检查完成
echo ==============================================================
echo.
echo [下一步] 启动程序...
echo.
pause

echo 启动程序中...
python pdf_to_word_gui.py

if errorlevel 1 (
    echo.
    echo [错误] 程序启动失败
    echo 请将上面的错误信息发送给我
) else (
    echo.
    echo [完成] 程序已正常退出
)
pause

