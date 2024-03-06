from PyQt5.QtWidgets import *

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setObjectName("MainPage")
        layout = QVBoxLayout()
        label = QLabel('Main Page')
        layout.addWidget(label)
        self.setLayout(layout)


