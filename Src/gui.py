import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox
)
from main import normalize_path, generate_resources_core

class GCGResGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GCG资源生成器")
        self.setGeometry(100, 100, 600, 400)
        
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # 输出目录输入
        self.output_dir_label = QLabel("GCG-Res-Output目录:")
        self.output_dir_input = QLineEdit()
        self.output_dir_button = QPushButton("浏览...")
        self.output_dir_button.clicked.connect(lambda: self.browse_directory(self.output_dir_input))
        
        # Grasscutter源目录输入
        self.grasscutter_label = QLabel("Grasscutter-Res-Origin目录:")
        self.grasscutter_input = QLineEdit()
        self.grasscutter_button = QPushButton("浏览...")
        self.grasscutter_button.clicked.connect(lambda: self.browse_directory(self.grasscutter_input))
        
        # GCG源目录输入
        self.gcg_label = QLabel("GCG-Res-Origin目录:")
        self.gcg_input = QLineEdit()
        self.gcg_button = QPushButton("浏览...")
        self.gcg_button.clicked.connect(lambda: self.browse_directory(self.gcg_input))
        
        # 生成按钮
        self.generate_button = QPushButton("生成资源")
        self.generate_button.clicked.connect(self.generate_resources)
        
        # 添加到布局
        layout.addWidget(self.output_dir_label)
        layout.addWidget(self.output_dir_input)
        layout.addWidget(self.output_dir_button)
        layout.addWidget(self.grasscutter_label)
        layout.addWidget(self.grasscutter_input)
        layout.addWidget(self.grasscutter_button)
        layout.addWidget(self.gcg_label)
        layout.addWidget(self.gcg_input)
        layout.addWidget(self.gcg_button)
        layout.addWidget(self.generate_button)
        
        central_widget.setLayout(layout)
    
    def browse_directory(self, line_edit):
        directory = QFileDialog.getExistingDirectory(self, "选择目录")
        if directory:
            line_edit.setText(directory)
    
    def generate_resources(self):
        output_dir = normalize_path(self.output_dir_input.text())
        grasscutter_dir = normalize_path(self.grasscutter_input.text())
        gcg_dir = normalize_path(self.gcg_input.text())
        
        if not all([output_dir, grasscutter_dir, gcg_dir]):
            QMessageBox.warning(self, "警告", "请填写所有目录路径")
            return
        
        try:
            generate_resources_core(output_dir, grasscutter_dir, gcg_dir)
            QMessageBox.information(self, "成功", "资源生成完成")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"资源生成失败: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GCGResGeneratorGUI()
    window.show()
    sys.exit(app.exec_())