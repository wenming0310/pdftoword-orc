import sys
import os
import site

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar, QTextEdit,
    QCheckBox, QGroupBox, QLineEdit, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

import fitz  # PyMuPDF
from pdf2docx import Converter
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
from docx import Document
from docx.shared import Inches


class PDFConverterThread(QThread):
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, pdf_path, output_path, use_ocr=False, detect_formulas=False, use_markdown=True, save_intermediate=False):
        super().__init__()
        self.pdf_path = pdf_path
        self.output_path = output_path
        self.use_ocr = use_ocr
        self.detect_formulas = detect_formulas
        self.use_markdown = use_markdown
        self.save_intermediate = save_intermediate

    def run(self):
        try:
            if self.use_ocr and not self.detect_formulas:
                self._convert_ocr_direct()
            elif self.use_markdown and self.detect_formulas:
                self._convert_with_markdown()
            else:
                self._convert_direct()
        except Exception as e:
            self.finished.emit(False, f"Conversion failed: {str(e)}")
    
    def _convert_ocr_direct(self):
        """Fast path: OCR directly to Word, no Markdown"""
        self.status_update.emit("Converting PDF with OCR...")
        self.progress_update.emit(10)
        
        doc = fitz.open(self.pdf_path)
        word_doc = Document()
        total_pages = len(doc)
        
        for page_num in range(total_pages):
            progress = 10 + int((page_num / total_pages) * 80)
            self.progress_update.emit(progress)
            
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            try:
                text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            except:
                try:
                    text = pytesseract.image_to_string(img, lang='eng')
                except:
                    text = page.get_text()
            
            if text.strip():
                word_doc.add_paragraph(text)
            
            if page_num < total_pages - 1:
                word_doc.add_page_break()
        
        doc.close()
        self.progress_update.emit(95)
        
        word_doc.save(self.output_path)
        self.progress_update.emit(100)
        self.finished.emit(True, "OCR conversion completed!")
    
    def _convert_with_markdown(self):
        """Use Markdown pipeline for formula detection"""
        from pdf_to_markdown import PDFToMarkdown, save_markdown
        from markdown_to_word import MarkdownToWord
        
        self.status_update.emit("Converting PDF to Markdown...")
        self.progress_update.emit(5)
        
        pdf2md = PDFToMarkdown(self.pdf_path, output_dir='temp_images')
        markdown = pdf2md.convert(
            use_ocr=self.use_ocr, 
            detect_formulas=self.detect_formulas,
            progress_callback=self.progress_update.emit
        )
        self.progress_update.emit(50)
        
        if self.save_intermediate:
            md_path = self.output_path.replace('.docx', '.md')
            save_markdown(markdown, md_path)
            self.status_update.emit(f"Markdown saved to: {md_path}")
        
        self.progress_update.emit(75)
        self.status_update.emit("Converting Markdown to Word...")
        
        md2word = MarkdownToWord(markdown, image_dir='temp_images')
        md2word.convert(self.output_path, progress_callback=self.progress_update.emit)
        
        self.progress_update.emit(100)
        self.finished.emit(True, "Conversion completed!")
    
    def _convert_direct(self):
        """Direct PDF to Word conversion"""
        self.status_update.emit("Converting PDF to Word...")
        self.progress_update.emit(50)
        
        cv = Converter(self.pdf_path)
        cv.convert(self.output_path, start=0, end=None)
        cv.close()
        
        self.progress_update.emit(100)
        self.finished.emit(True, "Conversion completed!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to Word Converter")
        self.setGeometry(100, 100, 900, 700)
        
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        
        pdf_layout = QHBoxLayout()
        self.pdf_path_label = QLabel("Select PDF file:")
        self.pdf_path_edit = QLineEdit()
        self.pdf_browse_btn = QPushButton("Browse...")
        self.pdf_browse_btn.clicked.connect(self.browse_pdf)
        pdf_layout.addWidget(self.pdf_path_label)
        pdf_layout.addWidget(self.pdf_path_edit)
        pdf_layout.addWidget(self.pdf_browse_btn)
        
        output_layout = QHBoxLayout()
        self.output_path_label = QLabel("Save as:")
        self.output_path_edit = QLineEdit()
        self.output_browse_btn = QPushButton("Browse...")
        self.output_browse_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.output_path_label)
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(self.output_browse_btn)
        
        file_layout.addLayout(pdf_layout)
        file_layout.addLayout(output_layout)
        file_group.setLayout(file_layout)
        
        options_group = QGroupBox("Conversion Options")
        options_layout = QVBoxLayout()
        
        self.use_ocr_check = QCheckBox("Use OCR (for scanned PDFs) - FAST")
        self.detect_formulas_check = QCheckBox("Detect and process formulas - SLOW")
        self.save_intermediate_check = QCheckBox("Save intermediate Markdown file (only if formulas detected)")
        
        options_layout.addWidget(self.use_ocr_check)
        options_layout.addWidget(self.detect_formulas_check)
        options_layout.addWidget(self.save_intermediate_check)
        options_group.setLayout(options_layout)
        
        info_label = QLabel("⚠️  Note: 'Detect and process formulas' will use a slower pipeline")
        info_label.setStyleSheet("color: orange; font-size: 11px;")
        
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.start_conversion)
        
        self.progress_bar = QProgressBar()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        layout.addWidget(file_group)
        layout.addWidget(options_group)
        layout.addWidget(info_label)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_text)

    def browse_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.pdf_path_edit.setText(file_path)
            self.output_path_edit.setText(file_path.replace(".pdf", ".docx"))

    def browse_output(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Word Documents (*.docx)")
        if file_path:
            self.output_path_edit.setText(file_path)

    def start_conversion(self):
        pdf_path = self.pdf_path_edit.text()
        output_path = self.output_path_edit.text()
        
        if not pdf_path or not output_path:
            QMessageBox.warning(self, "Warning", "Please select PDF file and output path!")
            return
        
        if not os.path.exists(pdf_path):
            QMessageBox.warning(self, "Warning", "PDF file not found!")
            return
        
        self.convert_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        
        self.thread = PDFConverterThread(
            pdf_path, 
            output_path,
            self.use_ocr_check.isChecked(),
            self.detect_formulas_check.isChecked(),
            True,
            self.save_intermediate_check.isChecked()
        )
        self.thread.progress_update.connect(self.update_progress)
        self.thread.status_update.connect(self.log_message)
        self.thread.finished.connect(self.conversion_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def log_message(self, message):
        self.log_text.append(message)

    def conversion_finished(self, success, message):
        self.convert_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)
        self.log_text.append(message)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
