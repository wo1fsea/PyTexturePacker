import sys
from PyQt6.QtWidgets import QMainWindow, QToolBar, QTreeView, QListView, QSplitter, QGraphicsView, QApplication, \
    QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QSpinBox, QHBoxLayout, QPushButton
from PyQt6.QtGui import QAction  # 正确的导入方式

from PyTexturePacker import Project


class PackerArgsWidget(QWidget):
    def __init__(self, packer_args, parent=None):
        super().__init__(parent)
        self.packer_args = packer_args
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 动态创建属性编辑器
        for attr, value in vars(self.packer_args).items():
            hbox = QHBoxLayout()
            label = QLabel(attr)
            hbox.addWidget(label, 2)
            if isinstance(value, bool):
                checkbox = QCheckBox()
                checkbox.setChecked(value)
                checkbox.stateChanged.connect(lambda state, attr=attr: self.updateAttribute(attr, state == Qt.Checked))
                hbox.addWidget(checkbox, 3)
            elif isinstance(value, int):
                spin_box = QSpinBox()
                spin_box.setValue(value)
                spin_box.setMaximum(9999)  # 根据需要调整最大值
                spin_box.valueChanged.connect(lambda value, attr=attr: self.updateAttribute(attr, value))
                hbox.addWidget(spin_box, 3)
            elif isinstance(value, str):
                line_edit = QLineEdit(value)
                line_edit.textChanged.connect(lambda value, attr=attr: self.updateAttribute(attr, value))
                hbox.addWidget(line_edit, 3)
            layout.addLayout(hbox, 1)

        self.setLayout(layout)

    def updateAttribute(self, attr, value):
        # 更新PackerArgs对象的属性
        if isinstance(value, int) or isinstance(value, str):
            setattr(self.packer_args, attr, value)
        elif isinstance(value, int):  # 对于复选框
            setattr(self.packer_args, attr, bool(value))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Interface Example")
        self.setGeometry(100, 100, 800, 600)

        # 创建上方工具栏
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        action = QAction("New", self)
        toolbar.addAction(action)

        # 创建主要布局
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # 创建左侧文件树
        self.tree_view = QTreeView()

        # 创建中间图片区域
        self.graphics_view = QGraphicsView()

        # 创建右侧属性列表
        self.list_view = PackerArgsWidget(Project.PackerArgs())

        # 使用QSplitter来分割左侧文件树、中间图片区域和右侧属性列表
        splitter = QSplitter()
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.graphics_view)
        splitter.addWidget(self.list_view)
        splitter.setSizes([150, 400, 200])

        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
