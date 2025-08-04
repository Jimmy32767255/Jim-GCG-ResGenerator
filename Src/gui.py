import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox,
    QRadioButton, QButtonGroup
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

        # 启用回退语言复选框
        self.enable_fallback_language_checkbox = QCheckBox("启用回退语言")
        self.enable_fallback_language_checkbox.setChecked(False) # 默认不启用

        # 生成选项单选框
        self.generate_all_radio = QRadioButton("生成所有资源")
        self.generate_no_json_name_radio = QRadioButton("不生成无Json名称资源")
        self.generate_no_text_map_name_radio = QRadioButton("不生成无正式名称资源")

        # 默认选中“生成所有资源”
        self.generate_all_radio.setChecked(True)

        # 将单选框添加到按钮组，确保只有一个可以被选中
        self.generate_option_group = QButtonGroup(self)
        self.generate_option_group.addButton(self.generate_all_radio)
        self.generate_option_group.addButton(self.generate_no_json_name_radio)
        self.generate_option_group.addButton(self.generate_no_text_map_name_radio)
        
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
        layout.addWidget(self.enable_fallback_language_checkbox)
        layout.addWidget(self.generate_all_radio)
        layout.addWidget(self.generate_no_json_name_radio)
        layout.addWidget(self.generate_no_text_map_name_radio)
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
        
        enable_fallback_language = self.enable_fallback_language_checkbox.isChecked()
        generate_all = self.generate_all_radio.isChecked()
        not_generate_no_json_name_res = self.generate_no_json_name_radio.isChecked()
        not_generate_no_text_map_name_res = self.generate_no_text_map_name_radio.isChecked()

        try:
            generate_resources_core(output_dir, grasscutter_dir, gcg_dir, 
                                    enable_fallback_language=enable_fallback_language,
                                    generate_all=generate_all,
                                    not_generate_no_json_name_res=not_generate_no_json_name_res,
                                    not_generate_no_text_map_name_res=not_generate_no_text_map_name_res)
            QMessageBox.information(self, "成功", "资源生成完成")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"资源生成失败: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GCGResGeneratorGUI()
    window.show()
    sys.exit(app.exec_())