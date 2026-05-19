import sys
import os
import site

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar, QTextEdit,
    QCheckBox, QGroupBox, QLineEdit, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Import the new conversion modules
from pdf_to_markdown import PDFToMarkdown, save_markdown
from markdown_to_word import MarkdownToWord
from pdf2docx import Converter


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
            if self.use_markdown:
                # Use the new PDF → Markdown → Word pipeline
                self.status_update.emit("Converting PDF to Markdown...")
                self.progress_update.emit(25)
                
                pdf2md = PDFToMarkdown(self.pdf_path, output_dir='temp_images')
                markdown = pdf2md.convert(use_ocr=self.use_ocr, detect_formulas=self.detect_formulas)
                self.progress_update.emit(50)
                
                # Save intermediate Markdown if needed
                if self.save_intermediate:
                    md_path = self.output_path.replace('.docx', '.md')
                    save_markdown(markdown, md_path)
                    self.status_update.emit(f"Markdown saved to: {md_path}")
                
                self.progress_update.emit(75)
                self.status_update.emit("Converting Markdown to Word...")
                
                md2word = MarkdownToWord(markdown, image_dir='temp_images')
                md2word.convert(self.output_path)
                
                self.progress_update.emit(100)
                self.finished.emit(True, f"Conversion completed! (using Markdown pipeline)")
            else:
                # Use the original pdf2docx directly
                self.status_update.emit("Converting PDF to Word directly...")
                self.progress_update.emit(50)
                
                cv = Converter(self.pdf_path)
                cv.convert(self.output_path, start=0, end=None)
                cv.close()
                
                self.progress_update.emit(100)
                self.finished.emit(True, "Conversion completed! (direct conversion)")
                
        except Exception as e:
            self.finished.emit(False, f"Conversion failed: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to Word Converter (with Markdown Pipeline)")
        self.setGeometry(100, 100, 900, 700)
        
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # File selection group
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
        
        # Options group
        options_group = QGroupBox("Conversion Options")
        options_layout = QVBoxLayout()
        
        self.use_ocr_check = QCheckBox("Use OCR (for scanned PDFs)")
        self.detect_formulas_check = QCheckBox("Detect and process formulas")
        self.use_markdown_check = QCheckBox("Use Markdown pipeline (improved accuracy)")
        self.use_markdown_check.setChecked(True)
        self.save_intermediate_check = QCheckBox("Save intermediate Markdown file")
        
        options_layout.addWidget(self.use_ocr_check)
        options_layout.addWidget(self.detect_formulas_check)
        options_layout.addWidget(self.use_markdown_check)
        options_layout.addWidget(self.save_intermediate_check)
        options_group.setLayout(options_layout)
        
        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.start_conversion)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        
        # Log area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        layout.addWidget(file_group)
        layout.addWidget(options_group)
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
            self.use_markdown_check.isChecked(),
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
