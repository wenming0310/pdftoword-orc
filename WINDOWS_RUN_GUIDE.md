
# PDF转Word带界面程序 - Windows本地运行指南

## 项目简介
这是一个带图形界面的Python程序，支持将带公式的PDF文件和PDF扫描件转换为Word文档。

## 环境要求
- Windows 7/8/10/11
- Python 3.7 或更高版本
- Tesseract OCR引擎（用于OCR功能）

## Windows本地运行步骤

### 1. 下载项目
将项目文件夹（包含以下文件）复制到您的Windows电脑上：
- `pdf_to_word_gui.py` - 主程序
- `formula_processor.py` - 公式处理模块
- `requirements.txt` - Python依赖库
- `README.md` - 项目说明
- `.gitignore` - Git忽略文件

### 2. 安装Python
1. 访问 https://www.python.org/downloads/
2. 下载并安装最新版Python（建议3.10+）
3. **重要**：安装时勾选 "Add Python to PATH"

### 3. 安装Tesseract OCR（可选，用于OCR功能）
1. 访问 https://github.com/UB-Mannheim/tesseract/wiki
2. 下载并安装Tesseract OCR
3. 安装时记下安装路径（通常是 `C:\Program Files\Tesseract-OCR`）

### 4. 创建虚拟环境（推荐）
打开命令提示符（CMD）或PowerShell，进入项目文件夹，运行：

```cmd
cd D:\zwm\python\PDF转Word带界面程序
python -m venv venv
```

### 5. 激活虚拟环境
- CMD:
  ```cmd
  venv\Scripts\activate.bat
  ```
- PowerShell:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### 6. 安装依赖库
```cmd
pip install -r requirements.txt
```

### 7. 配置Tesseract路径（如果安装了）
编辑 `pdf_to_word_gui.py`，在文件开头添加：

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 8. 运行程序
```cmd
python pdf_to_word_gui.py
```

## 使用说明
1. 点击 **"选择PDF文件"** 选择要转换的PDF
2. 点击 **"设置输出路径"** 指定保存的Word文档位置
3. 根据需要勾选：
   - **"使用OCR模式"** - 适用于PDF扫描件
   - **"检测和处理公式"** - 适用于包含数学公式的PDF
4. 点击 **"开始转换"** 进行转换
5. （可选）点击 **"同步到GitHub"** 提交代码

## 快速测试
如果您想先测试程序而不运行完整GUI，可以使用我们创建的测试脚本：

```cmd
python test_core_functions.py
python test_conversion_cli.py
```

## 常见问题
1. **模块导入错误**：确保已激活虚拟环境并安装了所有依赖
2. **GUI无法显示**：确保Python安装包含了tkinter（标准Python安装默认包含）
3. **OCR功能不工作**：检查Tesseract是否正确安装并配置了路径

## 技术支持
如有问题，请查看 `README.md` 文件获取更多详细信息。

