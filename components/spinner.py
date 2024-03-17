import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class SpinnerDialog(QDialog):
   def __init__(self, label):
      super().__init__()

      self.setWindowTitle("Spinner Example")
      self.setGeometry(100, 100, 400, 200)

      layout = QVBoxLayout()
      layout.setSpacing(20)
      layout.setContentsMargins(40, 40, 40, 40)

      self.progress_bar = QProgressBar()
      self.progress_bar.setAlignment(Qt.AlignCenter)
      self.progress_bar.setRange(0, 0)

      self.progress_bar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

      self.label = QLabel(label)
      self.label.setAlignment(Qt.AlignCenter)
      self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

      layout.addWidget(self.label)
      layout.addWidget(self.progress_bar)

      self.setLayout(layout)
      
      with open('styles/spinner_styles.qss', 'r') as style_file:
         self.setStyleSheet(style_file.read())