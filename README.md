# PDF转Word转换器

一个带图形界面的Python程序，支持将带公式的PDF文件和PDF扫描件转换为Word文档。

## 功能特性

- **普通PDF转换**：使用pdf2docx库将可编辑的PDF文件转换为Word文档
- **OCR模式**：使用Tesseract OCR引擎处理PDF扫描件
- **公式检测**：识别和处理PDF中的数学公式
- **友好的图形界面**：基于PyQt5构建，操作简单直观
- **进度显示**：实时显示转换进度

## 安装依赖

```bash
pip install -r requirements.txt
```

此外，还需要安装Tesseract OCR引擎：
- **Windows**: 下载并安装 [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

## 使用方法

1. 运行程序：
```bash
python pdf_to_word_gui.py
```

2. 在界面中：
   - 点击"选择PDF文件"选择要转换的PDF
   - 点击"设置输出路径"指定保存的Word文档位置
   - 根据需要勾选"使用OCR模式"（适用于扫描件）或"检测和处理公式"
   - 点击"开始转换"进行转换

## 项目结构

```
.
├── pdf_to_word_gui.py    # 主程序文件，包含GUI和转换逻辑
├── formula_processor.py  # 公式处理模块
├── requirements.txt      # Python依赖库列表
└── README.md            # 项目说明文档
```

## 技术栈

- **GUI框架**: PyQt5
- **PDF处理**: PyMuPDF (fitz), pdf2docx
- **OCR**: Tesseract (pytesseract)
- **Word文档**: python-docx
- **版本控制**: GitPython

## 注意事项

- 对于扫描件PDF，请确保勾选"使用OCR模式"
- 公式识别功能目前支持基本的数学符号检测
- 大文件转换可能需要较长时间，请耐心等待
