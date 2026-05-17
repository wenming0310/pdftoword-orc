#!/usr/bin/env python3
"""
简单的Tesseract OCR测试
"""
import sys

def test_tesseract():
    print("=" * 60)
    print("测试Tesseract OCR配置")
    print("=" * 60)
    
    # 1. 检查pytesseract是否可导入
    print("\n[1] 检查pytesseract模块...")
    try:
        import pytesseract
        print("✓ pytesseract导入成功")
    except ImportError as e:
        print(f"✗ pytesseract导入失败: {e}")
        print("\n解决方案：运行 pip install pytesseract")
        return False
    
    # 2. 检查tesseract_cmd配置
    print("\n[2] 检查tesseract_cmd配置...")
    try:
        tesseract_path = pytesseract.pytesseract.tesseract_cmd
        print(f"当前配置: {tesseract_path}")
    except Exception as e:
        print(f"✗ 无法读取tesseract_cmd: {e}")
        # 使用默认路径
        tesseract_path = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
        print(f"使用默认路径: {tesseract_path}")
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # 3. 检查文件是否存在
    print("\n[3] 检查Tesseract可执行文件...")
    import os
    if os.path.exists(tesseract_path):
        print(f"✓ 文件存在: {tesseract_path}")
    else:
        print(f"✗ 文件不存在: {tesseract_path}")
        print("\n可能的位置:")
        paths_to_check = [
            r"D:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for path in paths_to_check:
            if os.path.exists(path):
                print(f"✓ 找到Tesseract: {path}")
                print(f"\n请更新代码中的路径为:")
                print(f"pytesseract.pytesseract.tesseract_cmd = r'{path}'")
                return False
        return False
    
    # 4. 尝试运行tesseract --version
    print("\n[4] 测试Tesseract命令行...")
    try:
        import subprocess
        result = subprocess.run(
            [tesseract_path, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Tesseract命令行工作正常")
            print(f"版本信息: {result.stdout.strip()}")
        else:
            print(f"✗ Tesseract命令行返回错误")
            print(f"错误信息: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 无法运行Tesseract: {e}")
        return False
    
    # 5. 尝试简单的OCR测试
    print("\n[5] 测试OCR功能...")
    try:
        from PIL import Image
        import numpy as np
        
        # 创建测试图像
        print("创建测试图像...")
        img = Image.new('RGB', (300, 100), color='white')
        
        # 使用pytesseract识别
        print("运行OCR识别...")
        text = pytesseract.image_to_string(img, lang='eng')
        print(f"✓ OCR识别成功")
        print(f"识别的文本: {repr(text.strip())}")
        
        return True
        
    except Exception as e:
        print(f"✗ OCR识别失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tesseract()
    print("\n" + "=" * 60)
    if success:
        print("✓ Tesseract OCR测试全部通过！")
    else:
        print("✗ Tesseract OCR测试失败，请检查上述错误信息")
    print("=" * 60)
    input("\n按Enter键退出...")

