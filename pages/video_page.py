from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDateTime
import firebase

class VideoPage(QWidget):
    def __init__(self,user):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        INPUT_WIDTH = 300
        layout = QVBoxLayout()
        
        video_frame = QFrame()
        video_layout = QVBoxLayout()
        
        self.video_label = QLabel('Video Uploading & Processing')
        self.video_label.setObjectName("video_label")
        self.video_label.setAlignment(Qt.AlignHCenter)
        self.video_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        layout.addWidget(self.video_label, alignment=Qt.AlignHCenter)
        
        video_upload_form_layout = QFormLayout()
        video_upload_form_layout.setSpacing(40)
        
        self.video_upload_description = QLabel('Please upload the video you want to process.')
        self.video_upload_description.setObjectName("video_upload_description")
        self.video_upload_description.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        self.upload_video_label = QLabel('Upload Video')
        self.upload_video_label.setObjectName("upload_video_label")
        self.upload_video_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        self.upload_video_button = QPushButton('Upload Video')
        self.upload_video_button.setObjectName("upload_video_button")
        self.upload_video_button.clicked.connect(self.upload_video)
        
        self.set_datetime_label = QLabel('Set Date and Time')
        self.set_datetime_label.setObjectName("set_datetime_label")
        self.set_datetime_input = QDateTimeEdit()
        self.set_datetime_input.setFixedWidth(INPUT_WIDTH)
        self.set_datetime_input.setDateTime(QDateTime.currentDateTime())

        self.choose_store_label = QLabel('Choose Store')
        self.choose_store_label.setObjectName("choose_store_label")
        self.choose_store_input = QComboBox()
        self.choose_store_input.setFixedWidth(INPUT_WIDTH)
        self.choose_store_input.setPlaceholderText('Choose store')
        self.choose_store_input.addItems(firebase.getStoreNames(self.user))
        
        video_upload_form_layout.addRow(self.upload_video_label, self.upload_video_button)
        video_upload_form_layout.addRow(self.set_datetime_label, self.set_datetime_input)
        video_upload_form_layout.addRow(self.choose_store_label, self.choose_store_input)
        
        process_video_button = QPushButton('Process Video')
        process_video_button.setObjectName("process_video_button")
        
        video_layout.addWidget(self.video_label)
        video_layout.addWidget(self.video_upload_description)
        video_layout.addLayout(video_upload_form_layout)
        video_layout.addWidget(process_video_button, alignment=Qt.AlignCenter)
        
        video_frame.setLayout(video_layout)
        
        layout.addWidget(video_frame, alignment=Qt.AlignHCenter)
        self.setLayout(layout)
        
        with open('styles/video_styles.qss', 'r') as style_file:
            self.setStyleSheet(style_file.read())
        
        
    def upload_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Video", "", "Video Files (*.mp4 *.avi)", options=options)
        if file_name:
            print("Uploaded video:", file_name)