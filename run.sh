#!/bin/bash
# 激活虚拟环境并运行PDF转Word转换器

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="$SCRIPT_DIR/venv"

# 检查虚拟环境是否存在
if [ ! -d "$VENV_PATH" ]; then
    echo "正在创建虚拟环境..."
    cd "$SCRIPT_DIR"
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source "$VENV_PATH/bin/activate"

# 检查依赖是否已安装
if ! pip show PyQt5 > /dev/null 2>&1; then
    echo "正在安装依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 运行程序
echo "启动PDF转Word转换器..."
python pdf_to_word_gui.py
