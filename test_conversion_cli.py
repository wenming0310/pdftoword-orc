
#!/usr/bin/env python3
# 命令行版本的PDF转换测试
import sys
import os
from pdf2docx import Converter
import fitz  # PyMuPDF
from docx import Document
from formula_processor import FormulaProcessor

def test_simple_conversion():
    print("=" * 60)
    print("测试简单PDF转Word功能")
    print("=" * 60)
    
    # 创建一个简单的PDF用于测试（我们直接使用一个已有的PDF，或者创建一个）
    # 这里我们将通过PyMuPDF创建一个简单的测试PDF
    test_pdf_path = "/workspace/simple_test.pdf"
    test_output_path = "/workspace/simple_test_output.docx"
    
    print(f"创建测试PDF: {test_pdf_path}")
    
    # 创建简单的PDF
    doc = fitz.open()
    page = doc.new_page()
    
    # 添加文本
    page.insert_text((72, 72), "测试PDF文档", fontsize=24)
    page.insert_text((72, 120), "这是一个用于测试的PDF文件。", fontsize=12)
    page.insert_text((72, 160), "1 + 1 = 2", fontsize=14)
    page.insert_text((72, 190), "E = mc²", fontsize=14)
    
    doc.save(test_pdf_path)
    doc.close()
    print(f"✓ 测试PDF创建成功")
    
    # 测试转换
    print(f"\n开始转换PDF到Word: {test_output_path}")
    try:
        cv = Converter(test_pdf_path)
        cv.convert(test_output_path, start=0, end=None)
        cv.close()
        print("✓ 转换成功！")
        
        # 验证输出文件
        if os.path.exists(test_output_path):
            print(f"✓ 输出文件存在: {test_output_path}")
            file_size = os.path.getsize(test_output_path)
            print(f"  文件大小: {file_size} 字节")
        else:
            print("✗ 输出文件不存在！")
    except Exception as e:
        print(f"✗ 转换失败: {e}")

def test_formula_processor():
    print("\n" + "=" * 60)
    print("测试公式处理器转换功能")
    print("=" * 60)
    test_pdf_path = "/workspace/simple_test.pdf"
    test_output_path2 = "/workspace/formula_test_output.docx"
    
    try:
        processor = FormulaProcessor()
        processor.process_pdf_with_formulas(test_pdf_path, test_output_path2, use_ocr=False)
        print("✓ 公式处理器转换成功！")
        
        if os.path.exists(test_output_path2):
            print(f"✓ 输出文件存在: {test_output_path2}")
    except Exception as e:
        print(f"✗ 公式处理器转换失败: {e}")

if __name__ == "__main__":
    test_simple_conversion()
    test_formula_processor()
    print("\n" + "=" * 60)
    print("所有转换测试完成！")
    print("=" * 60)

