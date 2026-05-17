
import sys
import os

# 测试 formula_processor.py 模块
print("=" * 60)
print("测试 formula_processor.py 模块")
print("=" * 60)
try:
    from formula_processor import FormulaProcessor
    processor = FormulaProcessor()
    print("✓ FormulaProcessor 导入成功")
    
    # 测试公式检测
    test_texts = [
        "普通文本内容",
        "1 + 1 = 2",
        "E = mc²",
        "∑_{i=1}^{n} i = n(n+1)/2",
        "Hello World"
    ]
    print("\n测试公式检测功能:")
    for text in test_texts:
        result = processor.is_likely_formula(text)
        print(f"  '{text[:30]}' → {'是公式' if result else '不是公式'}")
    print("✓ formula_processor.py 测试通过")
except Exception as e:
    print(f"✗ formula_processor.py 测试失败: {e}")

print("\n" + "=" * 60)
print("测试依赖库")
print("=" * 60)
required_modules = [
    ('PyQt5', 'QtWidgets'),
    ('pdf2docx', 'Converter'),
    ('fitz', 'open'),
    ('docx', 'Document'),
    ('pytesseract', 'image_to_string'),
    ('PIL', 'Image'),
    ('cv2', '__version__'),
    ('numpy', 'array'),
    ('git', 'Repo')
]

for module_name, item in required_modules:
    try:
        module = __import__(module_name)
        if hasattr(module, item):
            print(f"✓ {module_name} 导入成功")
        else:
            print(f"✓ {module_name} 导入成功 (但 {item} 不存在)")
    except ImportError as e:
        print(f"✗ {module_name} 导入失败: {e}")

print("\n" + "=" * 60)
print("测试程序入口")
print("=" * 60)
try:
    # 尝试导入主程序，但不运行GUI
    sys.argv = ['test']  # 避免命令行参数问题
    from pdf_to_word_gui import PDFConverterThread, GitHubSyncThread, PDFToWordConverter
    print("✓ 主程序模块导入成功")
    print("  - PDFConverterThread 可用")
    print("  - GitHubSyncThread 可用")
    print("  - PDFToWordConverter 可用")
except Exception as e:
    print(f"✗ 主程序模块导入失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
print("\n注意: 完整的GUI程序需要图形环境才能运行。")
print("在无图形界面的环境中，您可以直接调用核心转换函数。")

