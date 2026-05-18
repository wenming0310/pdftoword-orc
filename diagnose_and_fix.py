#!/usr/bin/env python3
"""
PDF转Word程序 - 问题诊断脚本
帮助检测和修复常见问题
"""
import sys
import os
import site

# 修复 PyQt5 Windows 平台插件问题
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(site.getsitepackages()[0], 'PyQt5', 'Qt6', 'plugins', 'platforms')
if not os.path.exists(os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(site.getsitepackages()[-1], 'PyQt5', 'Qt6', 'plugins', 'platforms')
if not os.path.exists(os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt6', 'plugins', 'platforms')

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def check_python_version():
    print_section("1. 检查Python版本")
    version = sys.version_info
    print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 7:
        print("✓ Python版本符合要求（需要3.7+）")
        return True
    else:
        print("✗ Python版本过低，建议升级到3.7或更高版本")
        return False

def check_required_modules():
    print_section("2. 检查必需的Python模块")
    required = [
        'PyQt5',
        'PyQt5.QtWidgets',
        'PyQt5.QtCore',
        'fitz',
        'pdf2docx',
        'pytesseract',
        'PIL',
        'docx',
        'cv2',
        'numpy'
    ]
    
    all_ok = True
    for module_name in required:
        try:
            __import__(module_name)
            print(f"✓ {module_name:<20} - 已安装")
        except ImportError:
            print(f"✗ {module_name:<20} - 未安装")
            all_ok = False
    
    return all_ok

def check_pyqt_platform():
    print_section("3. 检查PyQt5平台插件")
    try:
        import PyQt5
        from PyQt5.QtCore import QLibraryInfo
        print(f"✓ PyQt5 版本: {PyQt5.QtCore.PYQT_VERSION_STR}")
        
        # 尝试获取Qt插件路径
        try:
            plugins_path = QLibraryInfo.location(QLibraryInfo.PluginsPath)
            print(f"✓ Qt插件路径: {plugins_path}")
            
            # 检查平台插件是否存在
            import os
            platforms_path = os.path.join(plugins_path, 'platforms')
            if os.path.exists(platforms_path):
                print(f"✓ 平台插件目录存在")
                qwindows_dll = os.path.join(platforms_path, 'qwindows.dll')
                if os.path.exists(qwindows_dll):
                    print(f"✓ qwindows.dll 存在")
                else:
                    print(f"⚠ qwindows.dll 未找到")
            else:
                print(f"⚠ 平台插件目录不存在")
        except Exception as e:
            print(f"⚠ 无法获取Qt插件信息: {e}")
        
        return True
    except Exception as e:
        print(f"✗ PyQt5检查失败: {e}")
        print("\n  解决方案:")
        print("  1. 运行 修复依赖.bat 重新安装PyQt5")
        print("  2. 或者运行: pip install --upgrade PyQt5 PyQt5-tools")
        return False

def check_tesseract():
    print_section("4. 检查Tesseract OCR")
    tesseract_path = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # 检查配置文件中的路径
    try:
        import pytesseract
        configured_path = pytesseract.pytesseract.tesseract_cmd
        print(f"当前配置的路径: {configured_path}")
    except:
        print("未找到pytesseract配置")
        configured_path = None
    
    # 检查文件是否存在
    if os.path.exists(tesseract_path):
        print(f"✓ Tesseract安装文件存在: {tesseract_path}")
        return True
    else:
        print(f"✗ Tesseract安装文件不存在: {tesseract_path}")
        
        # 检查常见位置
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                print(f"✓ 找到Tesseract: {path}")
                print(f"\n请更新代码中的tesseract_cmd路径为:")
                print(f"  pytesseract.pytesseract.tesseract_cmd = r'{path}'")
                return False
        
        print("\n✗ 未找到Tesseract安装")
        print("  请下载并安装: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def test_pdf_conversion():
    print_section("5. 测试PDF转换功能")
    try:
        from pdf2docx import Converter
        import fitz
        
        # 创建一个简单的测试PDF
        print("创建测试PDF...")
        test_pdf = "test_conversion.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "测试文档", fontsize=24)
        page.insert_text((72, 120), "这是一行测试文本", fontsize=12)
        doc.save(test_pdf)
        doc.close()
        print(f"✓ 测试PDF创建成功: {test_pdf}")
        
        # 测试转换
        print("测试PDF到Word转换...")
        output_docx = "test_conversion.docx"
        cv = Converter(test_pdf)
        cv.convert(output_docx, start=0, end=None)
        cv.close()
        
        if os.path.exists(output_docx):
            size = os.path.getsize(output_docx)
            print(f"✓ 转换成功！输出文件: {output_docx} ({size} bytes)")
            
            # 清理测试文件
            os.remove(test_pdf)
            os.remove(output_docx)
            print("✓ 测试文件已清理")
            return True
        else:
            print("✗ 转换失败：输出文件未生成")
            return False
            
    except Exception as e:
        print(f"✗ 转换测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ocr():
    print_section("6. 测试OCR功能")
    try:
        import pytesseract
        from PIL import Image
        import numpy as np
        import os
        
        # 设置 tesseract 路径
        tesseract_path = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            print(f"✓ 设置Tesseract路径: {tesseract_path}")
        
        # 创建简单的测试图像
        print("创建测试图像...")
        img = Image.new('RGB', (200, 50), color='white')
        
        # 使用pytesseract进行OCR
        print("运行OCR测试...")
        text = pytesseract.image_to_string(img, lang='eng')
        print(f"✓ OCR功能正常工作")
        print(f"  识别的文本: {repr(text[:50])}")
        return True
        
    except Exception as e:
        print(f"✗ OCR测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_main_program():
    print_section("7. 检查主程序")
    try:
        print("尝试导入主程序模块...")
        import pdf_to_word_gui
        print("✓ 主程序模块导入成功")
        
        # 检查关键类是否存在
        if hasattr(pdf_to_word_gui, 'PDFToWordConverter'):
            print("✓ PDFToWordConverter类可用")
        if hasattr(pdf_to_word_gui, 'PDFConverterThread'):
            print("✓ PDFConverterThread类可用")
            
        return True
    except ImportError as e:
        print(f"✗ 主程序导入失败: {e}")
        print("\n可能的问题:")
        print("  1. 当前目录不是程序所在目录")
        print("  2. 缺少依赖库")
        print("  3. 文件名或路径问题")
        return False
    except Exception as e:
        print(f"✗ 主程序检查出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "=" * 60)
    print("  PDF转Word转换器 - 问题诊断工具")
    print("=" * 60)
    
    results = []
    
    # 运行所有检查
    results.append(("Python版本", check_python_version()))
    results.append(("必需模块", check_required_modules()))
    results.append(("PyQt5平台", check_pyqt_platform()))
    results.append(("Tesseract OCR", check_tesseract()))
    results.append(("PDF转换", test_pdf_conversion()))
    results.append(("OCR功能", test_ocr()))
    results.append(("主程序", check_main_program()))
    
    # 总结
    print_section("诊断总结")
    print("\n检查结果:")
    for name, status in results:
        status_str = "✓ 通过" if status else "✗ 失败"
        print(f"  {name:<15} {status_str}")
    
    all_passed = all(status for _, status in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("  ✓ 所有检查通过！程序应该可以正常运行")
        print("  运行程序: python pdf_to_word_gui.py")
    else:
        print("  ⚠ 部分检查失败，请根据上述信息修复问题")
        print("  修复后重新运行此诊断脚本")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

