import os
from datetime import datetime

from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QIcon, QMouseEvent
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QDialog,
    QPushButton,
    QLabel,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QRadioButton,
    QTextBrowser)

from getWindow import get_window_info
from styles import *
from worldMethods.resizeWindow import *
from worldMethods.puHun import ph


class WorkerThread(QThread):
    signal_output = pyqtSignal(str)  # 定义输出信号

    def __init__(self, hwnd, logAdd):
        super().__init__()
        self.hwnd = hwnd
        self.logAdd = logAdd

    def run(self):
        """ 线程主方法，执行耗时操作 """
        # 在此处替换为实际耗时操作
        left, top = get_window_position(self.hwnd, self.logAdd)
        set_window_size(self.hwnd, self.logAdd)
        ph(self.hwnd, left, top, self.logAdd)


class DraggableButton(QPushButton):
    released = pyqtSignal(QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMouseTracking(True)
        self.parent0 = parent
        self.drag_start_global = None
        self.initial_local_pos = None
        self.initial_widget_global = None
        self.hwnd = None
        self.title = None

    def mousePressEvent(self, event: QMouseEvent):
        self.parent0.placeholder.show()
        self.parent0.placeholder.setStyleSheet(placeholder_style)
        if event.button() == Qt.LeftButton:
            # 记录鼠标按下的全局坐标
            self.drag_start_global = event.globalPos()
            # 记录控件当前的全局坐标（关键步骤）
            self.initial_widget_global = self.mapToGlobal(QPoint(0, 0))
            self.setStyleSheet(mousePressEvent_style)
            # 设置为独立窗口（脱离父控件裁剪）
            self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
            # 显式设置窗口位置为当前全局坐标
            self.move(self.initial_widget_global)
            self.show()  # 必须重新显示窗口

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_start_global and (event.buttons() & Qt.LeftButton):
            # 计算全局偏移量
            delta = event.globalPos() - self.drag_start_global
            # 计算新全局坐标
            new_global_pos = self.initial_widget_global + delta
            # 移动窗口到新位置
            self.move(new_global_pos)
        super().mouseMoveEvent(event)

        # super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.parent0.placeholder.hide()

        self.setWindowFlags(Qt.SubWindow)
        self.setParent(self.parent())  # 重新绑定父控件
        self.show()

        if event.button() == Qt.LeftButton:
            # 发射释放时的全局坐标
            self.released.emit(event.globalPos())
            self.drag_start_global = None

        super().mouseReleaseEvent(event)


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("世界OL脚本")
        self.resize(900, 439)
        self.setup_ui()
        self.worker = None
        self.windoWord = None
        self.windoName = None

    def setup_ui(self):
        # 主布局采用水平布局（左侧功能区 + 右侧日志）
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # ======== 左侧区域优化排版 ========
        # 拖动控制组（使用GroupBox容器）
        drag_group = QGroupBox("获取窗口句柄")

        drag_group.setStyleSheet(drag_group_style)
        drag_layout = QHBoxLayout()

        self.placeholder = QWidget()
        self.placeholder.setFixedSize(60, 60)
        self.placeholder.hide()

        self.drag_btn = DraggableButton(self)
        self.drag_btn.setIcon(QIcon(self.get_resource_path("aim.png")))  # 建议使用实际图标
        self.drag_btn.setIconSize(QSize(40, 40))
        self.drag_btn.setFixedSize(60, 60)
        self.drag_btn.setStyleSheet(drag_btn_style)

        self.drag_btn.released.connect(self.handle_drag_release)
        drag_info = QLabel("点击并长按拖拽按钮\n到目标窗口后释放")
        drag_info.setStyleSheet("color: #757575;")
        drag_info.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        drag_layout.addWidget(self.drag_btn)
        drag_layout.addWidget(self.placeholder)
        drag_layout.addWidget(drag_info)
        drag_group.setLayout(drag_layout)

        # 窗口信息组（表单布局）
        info_group = QGroupBox("窗口信息")
        info_group.setStyleSheet(info_group_style)
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(12)
        form_layout.setContentsMargins(15, 15, 15, 15)

        self.handle_edit = QLineEdit()
        self.handle_edit.setReadOnly(True)
        self.handle_edit.setPlaceholderText("窗口句柄...")
        self.handle_edit.setStyleSheet(handle_edit_style)

        self.name_edit = QLineEdit()
        self.name_edit.setReadOnly(True)
        self.name_edit.setPlaceholderText("窗口名称...")
        self.name_edit.setStyleSheet(self.handle_edit.styleSheet())

        form_layout.addRow(QLabel("窗口句柄:"), self.handle_edit)
        form_layout.addRow(QLabel("窗口名称:"), self.name_edit)
        info_group.setLayout(form_layout)

        # 选项组（带标题和边框）
        option_group = QGroupBox("操作选项")
        option_group.setStyleSheet(drag_group.styleSheet())
        option_layout = QVBoxLayout()
        option_layout.setSpacing(12)

        self.radio1 = QRadioButton("普混")
        self.radio2 = QRadioButton("敬请期待...")
        self.radio3 = QRadioButton("敬请期待...")

        for radio in [self.radio1, self.radio2, self.radio3]:
            radio.setStyleSheet(radio_style)
            option_layout.addWidget(radio)

        option_group.setLayout(option_layout)

        # 提示标签
        stop_layout = QHBoxLayout()
        # 初始化颜色列表
        self.colors = ['red', 'blue', 'green', 'brown']
        self.color_index = 0

        # 设置定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.changeColor)
        self.timer.timeout.connect(self.scrollText)
        self.timer.start(500)  # 每500毫秒改变一次颜色

        self.label_stop = QLabel(' Ctrl + D 强制停止进程')
        stop_layout.addWidget(self.label_stop)

        # 按钮组（底部对齐）
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("开始")
        self.btn_start.setEnabled(False)
        self.btn_start.setStyleSheet(btn_unable_style)
        self.btn_start.setFixedSize(80, 30)
        self.btn_clear = QPushButton("关闭")
        self.btn_clear.setFixedSize(80, 30)
        self.btn_clear.setStyleSheet(btn_able_style)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()

        # 组合左侧布局
        left_layout.addWidget(drag_group)
        left_layout.addWidget(info_group)
        left_layout.addWidget(option_group)
        left_layout.addLayout(stop_layout)
        left_layout.addLayout(btn_layout)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(15, 15, 15, 15)

        # ======== 右侧日志区域 ========

        self.log_browser = QTextBrowser()
        self.log_browser.setStyleSheet(log_style)
        right_layout.addWidget(QLabel("运行日志:"))
        right_layout.addWidget(self.log_browser)

        # 组合主布局
        # 组合主布局
        main_layout.addLayout(left_layout, stretch=2)  # 左侧占2份宽度
        main_layout.addLayout(right_layout, stretch=3)  # 右侧占3份宽度
        self.setLayout(main_layout)

        self.handle_edit.textChanged.connect(self.check_conditions)
        self.name_edit.textChanged.connect(self.check_conditions)
        self.radio1.toggled.connect(self.check_conditions)
        self.radio2.toggled.connect(self.check_conditions)
        self.radio3.toggled.connect(self.check_conditions)
        # 连接信号与槽
        self.btn_start.clicked.connect(self.start_task)
        # self.btn_start.clicked.connect(self.execute_method)
        self.btn_clear.clicked.connect(self.close_window)

    def execute_method(self):
        left, top = get_window_position(self.hwnd, self.logAdd)
        set_window_size(self.hwnd, self.logAdd)
        ph(self.hwnd, left, top, self.logAdd)
        # 这里可以添加你需要执行的代码

    def scrollText(self):
        scroll_bar = self.log_browser.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        self.log_browser.repaint()

    def close_window(self):
        self.close()

    def changeColor(self):
        # 更改 QLabel 的样式表来改变颜色
        self.label_stop.setStyleSheet(f"QLabel {{ color: {self.colors[self.color_index % len(self.colors)]}; }}")
        self.color_index += 1

    def check_conditions(self):
        # 获取输入内容（去除首尾空格）
        text1 = self.handle_edit.text().strip()
        text2 = self.name_edit.text().strip()

        # 检查条件
        has_text = bool(text1 and text2)
        radio_selected = self.radio1.isChecked(
        ) and not self.radio2.isChecked() and not self.radio3.isChecked()

        # 设置按钮状态
        self.btn_start.setEnabled(has_text and radio_selected)
        if has_text and radio_selected:
            self.btn_start.setStyleSheet(btn_able_style)
        else:
            self.btn_start.setStyleSheet(btn_unable_style)

    @pyqtSlot(QPoint)
    def handle_drag_release(self, pos):
        x, y = pos.x(), pos.y()
        self.logAdd(f"释放位置：[X: {x}, Y: {y}]")
        self.drag_btn.setStyleSheet(drag_btn_style)

        # 通过坐标获取坐标下的【窗口句柄】
        try:
            self.hwnd, self.title = get_window_info(x, y)  # 请填写 x 和 y 坐标
            if self.hwnd is not None and self.title != '':
                self.handle_edit.setText(str(self.hwnd))
                self.name_edit.setText(self.title)
                self.logAdd(f"成功获取窗口句柄")
            else:
                self.logAdd(f"所选位置不是窗口")
        except Exception as e:
            self.logAdd(f"Error occurred : {e}")

    def logAdd(self, txt):
        # 获取当前时间
        now = datetime.now()
        # 格式化为 "YYYY-MM-DD HH:MM:SS"
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S  ")

        self.log_browser.append(str(formatted_time) + txt)

    @pyqtSlot()
    def start_task(self):
        """ 启动任务 """
        self.worker = WorkerThread(self.hwnd, self.logAdd)
        self.worker.start()
        self.btn_start.setEnabled(False)
        self.btn_start.setStyleSheet(btn_unable_style)
        self.stop_task()

    @pyqtSlot()
    def stop_task(self):
        """ 结束任务 """
        self.btn_start.setEnabled(True)
        self.btn_start.setStyleSheet(btn_able_style)

    def get_resource_path(self,relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
