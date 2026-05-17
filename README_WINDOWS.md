# PDF转Word转换器 - Windows使用指南

## 快速开始

### 方法一：使用设置脚本（推荐）
1. 双击运行 `setup_windows.bat` 进行环境检查
2. 双击运行 `run_windows.bat` 启动程序

### 方法二：手动运行
1. 打开命令提示符（CMD）
2. 进入项目目录：`cd D:\zwm\python\PDF转Word带界面程序`
3. 创建虚拟环境（推荐）：`python -m venv venv`
4. 激活虚拟环境：`venv\Scripts\activate`
5. 安装依赖：`pip install -r requirements.txt`
6. 运行程序：`python pdf_to_word_gui.py`

## 功能说明

### 核心功能
- **普通PDF转换**：使用pdf2docx库将可编辑的PDF文件转换为Word文档
- **OCR模式**：使用Tesseract OCR引擎处理PDF扫描件
- **公式检测**：识别和处理PDF中的数学公式
- **友好的图形界面**：基于PyQt5构建，操作简单直观
- **进度显示**：实时显示转换进度
- **GitHub同步**：内置代码同步功能（需要安装Git）

### OCR功能（可选）
如需使用OCR功能，请安装Tesseract OCR：
1. 下载地址：https://github.com/UB-Mannheim/tesseract/wiki
2. 安装后，在 `pdf_to_word_gui.py` 文件开头添加：
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## 使用步骤

1. **选择PDF文件**：点击"选择PDF文件"按钮，选择要转换的PDF
2. **设置输出路径**：点击"设置输出路径"按钮，指定保存的Word文档位置
3. **选择转换模式**：
   - 不勾选：普通转换（适用于可编辑PDF）
   - 勾选"使用OCR模式"：OCR转换（适用于扫描件PDF）
   - 勾选"检测和处理公式"：公式识别转换（适用于包含数学公式的PDF）
4. **开始转换**：点击"开始转换"按钮
5. **查看结果**：转换完成后，日志区域会显示转换结果

## GitHub同步功能

程序内置了GitHub同步功能，可以方便地将代码提交到Git仓库。

### 启用GitHub同步
1. 安装Git for Windows：https://git-scm.com/download/win
2. 重启程序，GitHub按钮将自动启用

### 重要说明
- **Git功能是可选的**：即使没有安装Git，程序的核心转换功能仍然可以正常使用
- **GitHub按钮禁用提示**：如果没有安装Git，该按钮会显示为灰色并提示"Git不可用"
- **不影响转换功能**：即使Git不可用，您仍然可以使用所有PDF转换功能

## 常见问题

### Q1: 程序启动时报错"Bad git executable"
这是因为您的电脑没有安装Git或Git不在系统PATH中。

**解决方案**：
- **方案A（推荐）**：安装Git for Windows
  1. 下载：https://git-scm.com/download/win
  2. 安装时确保勾选"Add to PATH"
  3. 重启程序

- **方案B**：忽略Git功能
  - 程序已经修改为可以在没有Git的情况下运行
  - 只需忽略"同步到GitHub"按钮
  - 所有转换功能仍然正常

### Q2: OCR功能不工作
**检查步骤**：
1. 确认是否安装了Tesseract OCR
2. 确认 `tesseract_cmd` 路径是否正确
3. 确认是否选择了"使用OCR模式"

### Q3: 虚拟环境问题
**推荐做法**：
```cmd
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行程序
python pdf_to_word_gui.py
```

## 技术支持

### 查看详细文档
- `README.md` - 项目完整说明
- `WINDOWS_RUN_GUIDE.md` - Windows详细运行指南

### 测试程序
运行测试脚本验证功能：
```cmd
python test_core_functions.py
python test_conversion_cli.py
```

## 项目结构

```
.
├── pdf_to_word_gui.py      # 主程序文件，包含GUI和转换逻辑
├── formula_processor.py    # 公式处理模块
├── requirements.txt        # Python依赖库列表
├── README.md              # 项目说明文档
├── README_WINDOWS.md      # Windows使用指南（本文档）
├── WINDOWS_RUN_GUIDE.md    # Windows详细运行指南
├── setup_windows.bat      # Windows环境设置脚本
├── run_windows.bat        # Windows启动脚本
└── venv/                  # 虚拟环境（运行后生成）
```

## 注意事项

1. **大文件转换**：对于大型PDF文件，转换可能需要较长时间，请耐心等待
2. **公式识别**：公式识别功能目前支持基本的数学符号检测
3. **扫描件质量**：OCR功能对扫描件质量敏感，建议使用清晰的扫描件
4. **虚拟环境**：强烈建议使用虚拟环境，避免依赖冲突

## 依赖说明

核心依赖（必需）：
- PyQt5 - 图形界面
- pdf2docx - PDF转换
- pymupdf - PDF处理
- python-docx - Word文档创建
- numpy - 数值计算
- opencv-python - 图像处理
- Pillow - 图像处理

可选依赖：
- pytesseract - OCR识别（需要安装Tesseract OCR）
- gitpython - Git集成（需要安装Git）

