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
    
    def convert(self, use_ocr=True, detect_formulas=True):
        """Convert PDF to Markdown with optional OCR and formula detection"""
        doc = fitz.open(self.pdf_path)
        markdown_parts = []
        
        total_pages = len(doc)
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # Get page information
            page_info = f"\n<!-- Page {page_num + 1}/{total_pages} -->\n"
            markdown_parts.append(page_info)
            
            # Extract text from PDF directly
            direct_text = page.get_text().strip()
            
            # Get high-resolution image for OCR and formula detection
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            if use_ocr or detect_formulas:
                # Use OCR for better text extraction
                ocr_text = self._extract_text_ocr(img)
                
                if detect_formulas:
                    # Detect and extract formulas
                    formulas = self._extract_formulas(img, page_num)
                    
                    # Combine OCR text with formulas
                    combined_content = self._combine_text_and_formulas(
                        ocr_text or direct_text,
                        formulas
                    )
                    markdown_parts.append(combined_content)
                else:
                    markdown_parts.append(ocr_text or direct_text)
            else:
                # Use direct text extraction
                markdown_parts.append(direct_text)
            
            # Add page break
            markdown_parts.append("\n\n---\n\n")
        
        doc.close()
        
        # Combine all parts
        full_markdown = ''.join(markdown_parts)
        
        # Clean up temporary files
        self._cleanup_temp_files()
        
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
        """Extract formulas and return as markdown image references"""
        formulas = []
        
        img_np = np.array(img)
        
        # Method 1: OCR-based formula detection
        text_regions = self._detect_text_blocks_ocr(img_np)
        
        for region in text_regions:
            x, y, w, h, text = region
            if self._is_formula_text(text):
                # Save formula as image
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
        
        # Method 2: Image-based formula detection
        image_regions = self._detect_formula_by_image(img_np)
        
        for region in image_regions:
            x, y, w, h = region
            
            # Save formula as image
            formula_img = img.crop((x, y, x + w, y + h))
            formula_path = os.path.join(
                self.output_dir,
                f"formula_img_page{page_num + 1}_{x}_{y}.png"
            )
            formula_img.save(formula_path)
            
            formulas.append({
                'text': '[Formula detected]',
                'bbox': (x, y, w, h),
                'image_path': formula_path
            })
        
        return formulas
    
    def _detect_text_blocks_ocr(self, img_np):
        """Use Tesseract to detect text blocks"""
        try:
            img_pil = Image.fromarray(img_np)
            data = pytesseract.image_to_data(img_pil, output_type=pytesseract.Output.DICT)
            
            blocks = []
            n_boxes = len(data['text'])
            
            i = 0
            while i < n_boxes:
                if int(data['conf'][i]) > 30:
                    text = data['text'][i].strip()
                    if text:
                        x = data['left'][i]
                        y = data['top'][i]
                        w = data['width'][i]
                        h = data['height'][i]
                        
                        block_text = text
                        j = i + 1
                        while j < n_boxes and int(data['conf'][j]) > 30:
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
        """Check if text is likely a formula"""
        if not text or len(text.strip()) < 2:
            return False
        
        math_count = sum(1 for symbol in self.math_symbols if symbol in text)
        has_numbers = any(char.isdigit() for char in text)
        has_operators = any(op in text for op in ['+', '-', '×', '÷', '=', '/', '*'])
        has_fraction = bool(re.search(r'\d+/\d+', text))
        has_exponent = bool(re.search(r'\d+\^|\^\d+|\d+\*\*', text))
        has_greek = bool(re.search(r'[αβγδεζηθικλμνξοπρστυφχψω]', text, re.IGNORECASE))
        
        math_chars = sum(1 for c in text if c.isdigit() or c in '+-*/=<>≥≤≠()[]{}')
        math_ratio = math_chars / len(text) if len(text) > 0 else 0
        
        if math_count >= 2:
            return True
        if has_fraction or has_exponent:
            return True
        if has_greek and (has_numbers or has_operators):
            return True
        if math_ratio > 0.4 and has_numbers and has_operators:
            return True
        
        return False
    
    def _detect_formula_by_image(self, img_np):
        """Detect formulas using image processing"""
        formula_regions = []
        
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        detect_horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)
        
        contours, _ = cv2.findContours(
            detect_horizontal, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        img_height, img_width = img_np.shape[:2]
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w / 2
            is_centered = abs(center_x - img_width / 2) < img_width * 0.3
            is_wide = w > img_width * 0.3
            is_not_too_tall = h < img_height * 0.1
            
            if is_centered and is_wide and is_not_too_tall:
                formula_regions.append((x, y - 5, w, h + 10))
        
        return formula_regions
    
    def _combine_text_and_formulas(self, text, formulas):
        """Combine text with formula image references"""
        markdown = text
        
        for formula in formulas:
            # Insert formula image reference
            img_md = f"\n![{formula['text']}]({formula['image_path']})\n"
            markdown += img_md
        
        return markdown
    
    def _cleanup_temp_files(self):
        """Clean up temporary files if needed (will keep images for Word conversion)"""
        pass


def save_markdown(markdown, output_path):
    """Save markdown to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
