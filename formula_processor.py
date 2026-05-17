import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import pytesseract
from docx import Document
from docx.shared import Inches
import re


class FormulaProcessor:
    def __init__(self):
        pass

    def is_likely_formula(self, text):
        """判断文本是否可能是公式"""
        formula_keywords = ['=', '+', '-', '×', '÷', '∫', '∑', '∏', '√', '∞', '≠', '≤', '≥', '∈', '∪', '∩', '→', '←', '↔']
        math_symbols = 0
        for keyword in formula_keywords:
            math_symbols += text.count(keyword)
        
        has_numbers = any(char.isdigit() for char in text)
        has_letters = any(char.isalpha() for char in text)
        
        return math_symbols > 0 or (has_numbers and has_letters and len(text) > 5)

    def extract_formulas_from_pdf(self, pdf_path):
        """从PDF中提取可能包含公式的区域"""
        formulas = []
        pdf = fitz.open(pdf_path)
        
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            blocks = page.get_text("blocks")
            
            for block in blocks:
                x0, y0, x1, y1, text, block_no, block_type = block
                
                if self.is_likely_formula(text):
                    formulas.append({
                        'page': page_num,
                        'bbox': (x0, y0, x1, y1),
                        'text': text,
                        'position': (x0, y0)
                    })
        
        pdf.close()
        return formulas

    def process_pdf_with_formulas(self, pdf_path, output_path, use_ocr=False):
        """处理包含公式的PDF"""
        doc = Document()
        pdf = fitz.open(pdf_path)
        
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            if use_ocr:
                text = pytesseract.image_to_string(img, lang='chi_sim+eng')
                if text.strip():
                    doc.add_paragraph(text)
            else:
                text = page.get_text()
                if text.strip():
                    doc.add_paragraph(text)
            
            if page_num < len(pdf) - 1:
                doc.add_page_break()
        
        pdf.close()
        doc.save(output_path)
        return True
