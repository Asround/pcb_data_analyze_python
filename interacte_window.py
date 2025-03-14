import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import Parts as pt
import Projects as pjc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("数据分析工具")
        self.setGeometry(100, 100, 400, 300)

        # 主布局
        layout = QVBoxLayout()

        # 函数选择
        self.function_label = QLabel("选择函数:")
        layout.addWidget(self.function_label)

        self.function_combo = QComboBox()
        self.function_combo.addItems([
            "analyze_data",
            "analyze_data_windowed",
            "plot_multiple_files",
            "plot_multiple_files_windowed",
            "batch_analyze_data",
            "batch_analyze_data_windowed",
            "analyze_data_OutlierRemoval",
            "analyze_data_OutlierRemoval_windowed",
            "iterate_fitting_OutlierRemoval",
            "iterate_fitting_OutlierRemoval_windowed"
        ])
        layout.addWidget(self.function_combo)

        # 文件选择
        self.file_label = QLabel("选择文件:")
        layout.addWidget(self.file_label)

        self.file_button = QPushButton("选择文件")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        layout.addWidget(self.file_path)

        # 文件夹选择
        self.folder_label = QLabel("选择文件夹:")
        layout.addWidget(self.folder_label)

        self.folder_button = QPushButton("选择文件夹")
        self.folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_button)

        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        layout.addWidget(self.folder_path)

        # 执行按钮
        self.run_button = QPushButton("执行")
        self.run_button.clicked.connect(self.run_function)
        layout.addWidget(self.run_button)

        # 设置主窗口的中心部件
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.file_path.setText(file_path)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.folder_path.setText(folder_path)

    def run_function(self):
        function_name = self.function_combo.currentText()
        file_path = self.file_path.text()
        folder_path = self.folder_path.text()

        try:
            if function_name == "analyze_data":
                pjc.analyze_data(file_path)
            elif function_name == "analyze_data_windowed":
                pjc.analyze_data_windowed()
            elif function_name == "plot_multiple_files":
                pjc.plot_multiple_files(folder_path)
            elif function_name == "plot_multiple_files_windowed":
                pjc.plot_multiple_files_windowed()
            elif function_name == "batch_analyze_data":
                pjc.batch_analyze_data(folder_path)
            elif function_name == "batch_analyze_data_windowed":
                pjc.batch_analyze_data_windowed()
            elif function_name == "analyze_data_OutlierRemoval":
                pjc.analyze_data_OutlierRemoval(file_path)
            elif function_name == "analyze_data_OutlierRemoval_windowed":
                pjc.analyze_data_OutlierRemoval_windowed()
            elif function_name == "iterate_fitting_OutlierRemoval":
                pjc.iterate_fitting_OutlierRemoval(file_path)
            elif function_name == "iterate_fitting_OutlierRemoval_windowed":
                pjc.iterate_fitting_OutlierRemoval_windowed()
            else:
                QMessageBox.warning(self, "错误", "未选择有效的函数")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())