@echo off
echo ==============================================================
echo                  测试Tesseract OCR
echo ==============================================================
echo.
python -c "import pytesseract; print('Tesseract配置:', pytesseract.pytesseract.tesseract_cmd)"
echo.
if exist "D:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [OK] Tesseract可执行文件存在
) else (
    echo [FAIL] Tesseract未找到！
)
echo.
python -c "from PIL import Image; import pytesseract; img = Image.new('RGB', (100, 50)); t = pytesseract.image_to_string(img); print('[OK] OCR测试成功')"
echo.
pause

