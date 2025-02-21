import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QVBoxLayout, QLineEdit, QRadioButton,
                             QButtonGroup, QHBoxLayout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.check_conditions()  # 初始化时检查一次状态

    def initUI(self):
        # 窗口设置
        self.setWindowTitle('条件启用按钮示例')
        self.setGeometry(300, 300, 300, 200)

        # 创建控件
        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()

        self.radio1 = QRadioButton("选项1")
        self.radio2 = QRadioButton("选项2")
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)

        self.btn1 = QPushButton('执行操作')
        self.btn1.setEnabled(False)  # 初始不可用

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit1)
        layout.addWidget(self.lineEdit2)
        layout.addLayout(radio_layout)
        layout.addWidget(self.btn1)
        self.setLayout(layout)

        # 信号连接
        self.lineEdit1.textChanged.connect(self.check_conditions)
        self.lineEdit2.textChanged.connect(self.check_conditions)
        self.radio1.toggled.connect(self.check_conditions)
        self.radio2.toggled.connect(self.check_conditions)

    def check_conditions(self):
        # 获取输入内容（去除首尾空格）
        text1 = self.lineEdit1.text().strip()
        text2 = self.lineEdit2.text().strip()

        # 检查条件
        has_text = bool(text1 and text2)
        radio_selected = self.radio1.isChecked()

        # 设置按钮状态
        self.btn1.setEnabled(has_text and radio_selected)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
