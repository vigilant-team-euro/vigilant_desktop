from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class EmployeePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setObjectName("EmployeePage")
        layout = QVBoxLayout()
        label = QLabel('Employee Page')
        layout.addWidget(label)
        self.setLayout(layout)