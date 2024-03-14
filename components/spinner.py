import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class SpinnerDialog(QDialog):
   def __init__(self, label):
      super().__init__()

      self.setWindowTitle("Spinner Example")
      self.setGeometry(100, 100, 400, 300)

      layout = QVBoxLayout()

      self.progress_bar = QProgressBar()
      self.progress_bar.setAlignment(Qt.AlignHCenter)
      self.progress_bar.setRange(0, 0)
      self.progress_bar.setValue(0)
      
      self.label = QLabel(label)
      self.label.setAlignment(Qt.AlignHCenter)

      layout.addWidget(self.label)
      layout.addWidget(self.progress_bar)
      
      self.setLayout(layout)