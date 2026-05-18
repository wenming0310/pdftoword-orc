@echo off
chcp 65001 >nul
title 诊断 PyQt5 平台插件

echo ======================================
echo   诊断 PyQt5 平台插件问题
echo ======================================
echo.

echo 正在检查 Python 环境...
python -c "import sys; print(f'Python版本: {sys.version}')"
if errorlevel 1 (
    echo [FAIL] Python 未安装或未正确配置
    pause
    exit /b 1
)

echo.
echo 正在检查 PyQt5 安装...
python -c "import PyQt5; print(f'PyQt5版本: {PyQt5.QtCore.PYQT_VERSION_STR}')"
if errorlevel 1 (
    echo [FAIL] PyQt5 未安装
    echo 请运行: python -m pip install PyQt5
    pause
    exit /b 1
)

echo.
echo 正在检查 site-packages 路径...
python -c "import site; print('site-packages:', site.getsitepackages())"

echo.
echo 正在检查平台插件目录...
python -c "
import os
import site

paths = [
    os.path.join(site.getsitepackages()[0], 'PyQt5', 'Qt6', 'plugins', 'platforms'),
    os.path.join(site.getsitepackages()[-1], 'PyQt5', 'Qt6', 'plugins', 'platforms'),
    os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt6', 'plugins', 'platforms')
]

found = False
for path in paths:
    if os.path.exists(path):
        print(f'[OK] 找到平台插件目录: {path}')
        files = os.listdir(path)
        if 'qwindows.dll' in files:
            print(f'[OK] 找到 qwindows.dll')
            found = True
        else:
            print(f'[WARN] qwindows.dll 不存在于: {path}')
            print(f'  目录中的文件: {files}')
    else:
        print(f'[SKIP] 目录不存在: {path}')

if not found:
    print('[FAIL] 未找到 qwindows.dll')
    print('PyQt5 安装可能不完整')
    exit(1)
"

if errorlevel 1 (
    echo.
    echo [发现问题] PyQt5 平台插件缺失
    echo 尝试重新安装 PyQt5...
    python -m pip uninstall PyQt5 -y
    python -m pip install PyQt5
    if errorlevel 1 (
        echo [FAIL] 重新安装 PyQt5 失败
        pause
        exit /b 1
    )
)

echo.
echo ======================================
echo   测试 Qt 应用程序启动
echo ======================================
echo.

python -c "
import sys
import os
import site

# 设置插件路径
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(site.getsitepackages()[0], 'PyQt5', 'Qt6', 'plugins', 'platforms')
if not os.path.exists(os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(site.getsitepackages()[-1], 'PyQt5', 'Qt6', 'plugins', 'platforms')
if not os.path.exists(os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt6', 'plugins', 'platforms')

print(f'插件路径: {os.environ.get(\"QT_QPA_PLATFORM_PLUGIN_PATH\")}')

from PyQt5.QtWidgets import QApplication
app = QApplication([])
print('[OK] Qt 应用程序创建成功')
"

if errorlevel 1 (
    echo.
    echo [FAIL] Qt 应用程序启动失败
    echo.
    echo 可能的问题：
    echo 1. PyQt5 安装不完整
    echo 2. Windows Visual C++ Redistributable 未安装
    echo 3. 杀毒软件阻止了 DLL 加载
    echo.
    echo 建议：
    echo 1. 重新安装 PyQt5: python -m pip uninstall PyQt5 -y ^&^& python -m pip install PyQt5
    echo 2. 下载安装 Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
    pause
    exit /b 1
)

echo.
echo ======================================
echo   诊断完成
echo ======================================
echo [OK] PyQt5 平台插件检查通过
echo 现在可以运行程序: python pdf_to_word_gui.py
echo.
pause
