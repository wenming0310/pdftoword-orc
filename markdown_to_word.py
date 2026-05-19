from docx import Document
from docx.shared import Inches, Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
import re
import time


class MarkdownToWord:
    def __init__(self, markdown_text, image_dir='temp_images'):
        self.markdown_text = markdown_text
        self.image_dir = image_dir
        self.doc = Document()
        self.start_time = None
        
        # Set default style
        self._setup_document_style()
    
    def _setup_document_style(self):
        """Setup document default styles"""
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)
    
    def convert(self, output_path, progress_callback=None):
        """Convert Markdown to Word document"""
        self.start_time = time.time()
        lines = self.markdown_text.split('\n')
        total_lines = len(lines)
        
        i = 0
        while i < total_lines:
            line = lines[i].rstrip()
            
            if progress_callback and i % 100 == 0:
                progress = int((i / total_lines) * 25) + 75  # 75-100%
                progress_callback(progress)
            
            if line.startswith('# '):
                self._add_heading(line[2:], level=1)
            elif line.startswith('## '):
                self._add_heading(line[3:], level=2)
            elif line.startswith('### '):
                self._add_heading(line[4:], level=3)
            elif line.startswith('#### '):
                self._add_heading(line[5:], level=4)
            elif line.startswith('##### '):
                self._add_heading(line[6:], level=5)
            elif line.startswith('###### '):
                self._add_heading(line[7:], level=6)
            elif line.startswith('!['):
                self._add_image_fast(line)
            elif line.startswith('<!--'):
                pass
            elif line.startswith('---') or line.startswith('***'):
                self._add_horizontal_rule()
            elif line.startswith('- ') or line.startswith('* '):
                i = self._add_list(lines, i, 'bullet')
                continue
            elif re.match(r'^\d+\. ', line):
                i = self._add_list(lines, i, 'number')
                continue
            elif line.strip() == '':
                self.doc.add_paragraph()
            elif line.startswith('> '):
                self._add_quote(line[2:])
            elif line.startswith('```'):
                i = self._add_code_block(lines, i)
                continue
            else:
                if line.strip():
                    self._add_paragraph_fast(line)
            
            i += 1
        
        self.doc.save(output_path)
    
    def _add_heading(self, text, level):
        self.doc.add_heading(text, level=level)
    
    def _add_paragraph_fast(self, text):
        """Fast paragraph add without complex formatting"""
        # Skip complex formatting for speed - just add plain text
        self.doc.add_paragraph(text)
    
    def _add_image_fast(self, line):
        """Fast image add with timeout"""
        match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
        if match:
            alt_text, img_path = match.groups()
            
            if os.path.exists(img_path):
                try:
                    # Quick check - don't open the image if not needed
                    file_size = os.path.getsize(img_path)
                    
                    # Skip very small images (likely noise)
                    if file_size < 100:
                        self.doc.add_paragraph(f"[Image: {alt_text}]")
                        return
                    
                    # Add image without calculating size (let Word handle it)
                    paragraph = self.doc.add_paragraph()
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = paragraph.add_run()
                    
                    # Try with a default max width
                    try:
                        run.add_picture(img_path, width=Inches(5.0))
                    except:
                        # If fails, try without specifying size
                        try:
                            run.add_picture(img_path)
                        except Exception as e:
                            print(f"Error adding image {img_path}: {e}")
                            self.doc.add_paragraph(f"[Image: {alt_text}]")
                except Exception as e:
                    print(f"Error processing image {img_path}: {e}")
                    self.doc.add_paragraph(f"[Image: {alt_text}]")
            else:
                self.doc.add_paragraph(f"[Image: {alt_text}]")
    
    def _add_horizontal_rule(self):
        paragraph = self.doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.add_run('─' * 40)
    
    def _add_quote(self, text):
        paragraph = self.doc.add_paragraph(text)
        paragraph.paragraph_format.left_indent = Inches(0.5)
        paragraph.paragraph_format.right_indent = Inches(0.5)
    
    def _add_code_block(self, lines, start_idx):
        end_idx = start_idx + 1
        while end_idx < len(lines) and not lines[end_idx].startswith('```'):
            end_idx += 1
        
        code_lines = lines[start_idx + 1:end_idx]
        for line in code_lines:
            paragraph = self.doc.add_paragraph(line)
            paragraph.paragraph_format.left_indent = Inches(0.5)
            run = paragraph.runs[0]
            run.font.name = 'Courier New'
        
        return end_idx
    
    def _add_list(self, lines, start_idx, list_type):
        i = start_idx
        
        if list_type == 'bullet':
            while i < len(lines):
                line = lines[i].rstrip()
                if line.startswith('- ') or line.startswith('* '):
                    self.doc.add_paragraph(line[2:], style='List Bullet')
                    i += 1
                else:
                    break
        elif list_type == 'number':
            while i < len(lines):
                if re.match(r'^\d+\. ', lines[i]):
                    self.doc.add_paragraph(re.sub(r'^\d+\. ', '', lines[i]), style='List Number')
                    i += 1
                else:
                    break
        
        return i - 1
