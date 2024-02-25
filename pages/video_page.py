from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class VideoPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setObjectName("VideoPage")
        layout = QVBoxLayout()
        label = QLabel('Video Page')
        layout.addWidget(label)
        self.setLayout(layout)
        
        
        
        
        
def upload_video(self):
   options = QFileDialog.Options()
   options |= QFileDialog.DontUseNativeDialog
   file_name, _ = QFileDialog.getOpenFileName(self, "Upload Video", "", "Video Files (*.mp4 *.avi)", options=options)
   if file_name:
      print("Uploaded video:", file_name)