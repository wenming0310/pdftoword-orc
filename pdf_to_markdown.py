import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2
import os
import re


class PDFToMarkdown:
    def __init__(self, pdf_path, output_dir='temp_images'):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.math_symbols = [
            '=', '+', '-', '×', '÷', '∫', '∑', '∏', '√', '∞',
            '≠', '≤', '≥', '∈', '∪', '∩', '→', '←', '↔', '⇒',
            '∀', '∂', 'Δ', '∇', '⊂', '⊃', '⊆', '⊇', 'α', 'β',
            'γ', 'δ', 'ε', 'θ', 'λ', 'μ', 'π', 'σ', 'φ', 'ω'
        ]
        os.makedirs(output_dir, exist_ok=True)
    
    def convert(self, use_ocr=True, detect_formulas=True, progress_callback=None):
        """Convert PDF to Markdown with optional OCR and formula detection"""
        doc = fitz.open(self.pdf_path)
        markdown_parts = []
        
        total_pages = len(doc)
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            if progress_callback:
                progress = int((page_num / total_pages) * 50)
                progress_callback(progress)
            
            page_info = f"\n<!-- Page {page_num + 1}/{total_pages} -->\n"
            markdown_parts.append(page_info)
            
            direct_text = page.get_text().strip()
            
            if use_ocr or detect_formulas:
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))  # Reduce resolution for speed
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                ocr_text = self._extract_text_ocr(img)
                
                if detect_formulas:
                    formulas = self._extract_formulas(img, page_num)
                    combined_content = self._combine_text_and_formulas(
                        ocr_text or direct_text,
                        formulas
                    )
                    markdown_parts.append(combined_content)
                else:
                    markdown_parts.append(ocr_text or direct_text)
            else:
                markdown_parts.append(direct_text)
            
            markdown_parts.append("\n\n---\n\n")
        
        doc.close()
        full_markdown = ''.join(markdown_parts)
        return full_markdown
    
    def _extract_text_ocr(self, img):
        """Extract text using Tesseract OCR"""
        try:
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            return text.strip()
        except:
            try:
                text = pytesseract.image_to_string(img, lang='eng')
                return text.strip()
            except:
                return ""
    
    def _extract_formulas(self, img, page_num):
        """Extract formulas with limits on number of images"""
        formulas = []
        
        img_np = np.array(img)
        
        # Only use OCR-based detection, skip image-based for speed
        text_regions = self._detect_text_blocks_ocr(img_np)
        
        for region in text_regions:
            x, y, w, h, text = region
            
            # Only consider blocks with decent size
            if w < 50 or h < 20:
                continue
            
            if self._is_formula_text(text):
                # Skip if too many formulas already
                if len(formulas) >= 5:
                    break
                
                formula_img = img.crop((x - 10, y - 5, x + w + 10, y + h + 5))
                formula_path = os.path.join(
                    self.output_dir,
                    f"formula_page{page_num + 1}_{x}_{y}.png"
                )
                formula_img.save(formula_path)
                
                formulas.append({
                    'text': text,
                    'bbox': (x, y, w, h),
                    'image_path': formula_path
                })
        
        return formulas
    
    def _detect_text_blocks_ocr(self, img_np):
        """Use Tesseract to detect text blocks (simplified)"""
        try:
            img_pil = Image.fromarray(img_np)
            data = pytesseract.image_to_data(img_pil, output_type=pytesseract.Output.DICT)
            
            blocks = []
            n_boxes = len(data['text'])
            
            i = 0
            while i < n_boxes:
                if int(data['conf'][i]) > 40:  # Higher confidence threshold
                    text = data['text'][i].strip()
                    if text:
                        x = data['left'][i]
                        y = data['top'][i]
                        w = data['width'][i]
                        h = data['height'][i]
                        
                        block_text = text
                        j = i + 1
                        while j < n_boxes and int(data['conf'][j]) > 40:
                            next_text = data['text'][j].strip()
                            if next_text:
                                if abs(data['top'][j] - y) < h:
                                    block_text += ' ' + next_text
                                    w = max(w, data['left'][j] + data['width'][j] - x)
                                    j += 1
                                else:
                                    break
                            else:
                                j += 1
                        
                        if block_text.strip():
                            blocks.append((x, y, w, h, block_text))
                        i = j
                    else:
                        i += 1
                else:
                    i += 1
            
            return blocks
        except:
            return []
    
    def _is_formula_text(self, text):
        """Check if text is likely a formula (stricter)"""
        if not text or len(text.strip()) < 3:
            return False
        
        math_count = sum(1 for symbol in self.math_symbols if symbol in text)
        has_numbers = any(char.isdigit() for char in text)
        has_operators = any(op in text for op in ['+', '-', '×', '÷', '=', '/', '*'])
        has_fraction = bool(re.search(r'\d+/\d+', text))
        has_exponent = bool(re.search(r'\d+\^|\^\d+|\d+\*\*', text))
        has_greek = bool(re.search(r'[αβγδεζηθικλμνξοπρστυφχψω]', text, re.IGNORECASE))
        
        math_chars = sum(1 for c in text if c.isdigit() or c in '+-*/=<>≥≤≠()[]{}')
        math_ratio = math_chars / len(text) if len(text) > 0 else 0
        
        # Stricter requirements
        if math_count >= 3:
            return True
        if has_fraction and math_count >= 1:
            return True
        if has_greek and (has_numbers or has_operators):
            return True
        if math_ratio > 0.5 and has_numbers and has_operators and len(text) > 5:
            return True
        
        return False
    
    def _combine_text_and_formulas(self, text, formulas):
        """Combine text with formula image references"""
        markdown = text
        
        for formula in formulas:
            img_md = f"\n![{formula['text']}]({formula['image_path']})\n"
            markdown += img_md
        
        return markdown


def save_markdown(markdown, output_path):
    """Save markdown to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
