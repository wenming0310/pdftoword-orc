import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar, QTextEdit,
    QCheckBox, QGroupBox, QLineEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import fitz  # PyMuPDF
from pdf2docx import Converter
import pytesseract
from PIL import Image
import cv2
import numpy as np
from docx import Document
from docx.shared import Inches
import git
import requests


class PDFConverterThread(QThread):
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, pdf_path, output_path, use_ocr=False):
        super().__init__()
        self.pdf_path = pdf_path
        self.output_path = output_path
        self.use_ocr = use_ocr

    def run(self):
        try:
            if self.use_ocr:
                self.status_update.emit("正在使用OCR模式处理PDF...")
                self._convert_with_ocr()
            else:
                self.status_update.emit("正在转换PDF...")
                self._convert_with_pdf2docx()
            
            self.finished.emit(True, "转换完成！")
        except Exception as e:
            self.finished.emit(False, f"转换失败: {str(e)}")

    def _convert_with_pdf2docx(self):
        cv = Converter(self.pdf_path)
        total_pages = len(cv)
        
        def progress_callback(current, total):
            progress = int((current / total) * 100)
            self.progress_update.emit(progress)
            self.status_update.emit(f"正在处理第 {current} 页，共 {total} 页")
        
        cv.convert(self.output_path, start=0, end=None, callback=progress_callback)
        cv.close()
        self.progress_update.emit(100)

    def _convert_with_ocr(self):
        doc = Document()
        pdf = fitz.open(self.pdf_path)
        total_pages = pdf.page_count
        
        for page_num in range(total_pages):
            self.progress_update.emit(int((page_num / total_pages) * 100))
            self.status_update.emit(f"正在处理第 {page_num + 1} 页，共 {total_pages} 页")
            
            page = pdf[page_num]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            
            if text.strip():
                doc.add_paragraph(text)
            
            if page_num < total_pages - 1:
                doc.add_page_break()
        
        pdf.close()
        doc.save(self.output_path)
        self.progress_update.emit(100)


class GitHubSyncThread(QThread):
    status_update = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, repo_path, commit_message="更新代码"):
        super().__init__()
        self.repo_path = repo_path
        self.commit_message = commit_message

    def run(self):
        try:
            if not os.path.exists(os.path.join(self.repo_path, '.git')):
                self.status_update.emit("初始化Git仓库...")
                repo = git.Repo.init(self.repo_path)
            else:
                repo = git.Repo(self.repo_path)
            
            self.status_update.emit("添加文件到暂存区...")
            repo.git.add(A=True)
            
            self.status_update.emit("提交更改...")
            repo.index.commit(self.commit_message)
            
            self.finished.emit(True, "代码同步成功！")
        except Exception as e:
            self.finished.emit(False, f"同步失败: {str(e)}")


class PDFToWordConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF转Word转换器")
        self.setGeometry(100, 100, 800, 600)
        self.pdf_path = ""
        self.output_path = ""
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 文件选择区域
        file_group = QGroupBox("文件选择")
        file_layout = QVBoxLayout()

        # PDF文件选择
        pdf_layout = QHBoxLayout()
        self.pdf_label = QLabel("未选择PDF文件")
        pdf_button = QPushButton("选择PDF文件")
        pdf_button.clicked.connect(self.select_pdf)
        pdf_layout.addWidget(self.pdf_label)
        pdf_layout.addWidget(pdf_button)
        file_layout.addLayout(pdf_layout)

        # 输出路径选择
        output_layout = QHBoxLayout()
        self.output_label = QLabel("未设置输出路径")
        output_button = QPushButton("设置输出路径")
        output_button.clicked.connect(self.select_output)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(output_button)
        file_layout.addLayout(output_layout)

        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # 选项区域
        options_group = QGroupBox("转换选项")
        options_layout = QVBoxLayout()
        self.ocr_checkbox = QCheckBox("使用OCR模式（适用于扫描件）")
        options_layout.addWidget(self.ocr_checkbox)
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # 进度区域
        progress_group = QGroupBox("转换进度")
        progress_layout = QVBoxLayout()
        self.status_label = QLabel("就绪")
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.status_label)
        progress_layout.addWidget(self.progress_bar)
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)

        # 操作按钮
        button_layout = QHBoxLayout()
        self.convert_button = QPushButton("开始转换")
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setEnabled(False)
        self.github_button = QPushButton("同步到GitHub")
        self.github_button.clicked.connect(self.sync_to_github)
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.github_button)
        main_layout.addLayout(button_layout)

        # 日志区域
        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择PDF文件", "", "PDF文件 (*.pdf)")
        if file_path:
            self.pdf_path = file_path
            self.pdf_label.setText(os.path.basename(file_path))
            self.check_convert_button()
            self.log(f"已选择PDF文件: {file_path}")

    def select_output(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存Word文档", "", "Word文档 (*.docx)")
        if file_path:
            self.output_path = file_path
            self.output_label.setText(os.path.basename(file_path))
            self.check_convert_button()
            self.log(f"已设置输出路径: {file_path}")

    def check_convert_button(self):
        self.convert_button.setEnabled(bool(self.pdf_path and self.output_path))

    def start_conversion(self):
        self.convert_button.setEnabled(False)
        self.github_button.setEnabled(False)
        self.converter_thread = PDFConverterThread(
            self.pdf_path,
            self.output_path,
            self.ocr_checkbox.isChecked()
        )
        self.converter_thread.progress_update.connect(self.update_progress)
        self.converter_thread.status_update.connect(self.update_status)
        self.converter_thread.finished.connect(self.conversion_finished)
        self.converter_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, text):
        self.status_label.setText(text)
        self.log(text)

    def conversion_finished(self, success, message):
        self.convert_button.setEnabled(True)
        self.github_button.setEnabled(True)
        self.log(message)
        self.status_label.setText("就绪")
        if not success:
            self.status_label.setText("转换失败")

    def sync_to_github(self):
        self.convert_button.setEnabled(False)
        self.github_button.setEnabled(False)
        self.log("开始同步到GitHub...")
        self.github_thread = GitHubSyncThread(os.path.dirname(os.path.abspath(__file__)))
        self.github_thread.status_update.connect(self.update_status)
        self.github_thread.finished.connect(self.github_sync_finished)
        self.github_thread.start()

    def github_sync_finished(self, success, message):
        self.convert_button.setEnabled(True)
        self.github_button.setEnabled(True)
        self.log(message)
        if success:
            self.status_label.setText("同步完成")
        else:
            self.status_label.setText("同步失败")

    def log(self, message):
        self.log_text.append(message)


def main():
    app = QApplication(sys.argv)
    converter = PDFToWordConverter()
    converter.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
