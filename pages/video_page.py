from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDateTime, QObject, QThread, pyqtSignal
from components.spinner import SpinnerDialog
import computer_vision

class VideoPage(QWidget):
    def __init__(self, user_info):
        super().__init__()
        self.user = user_info['user']
        self.stores = user_info['stores'].keys()
        self.storeIds = user_info['stores']
        self.file_name = ""
        self.store_name = ""
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
        self.choose_store_input.addItems(self.stores)
        
        self.heatmap_label = QLabel('Generate Heatmap')
        self.heatmap_label.setObjectName("heatmap_label")
        self.heatmap_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        self.heatmap_checkbox = QCheckBox()
        self.heatmap_checkbox.setObjectName("heatmap_checkbox")
        self.heatmap_checkbox.setChecked(True)
        
        video_upload_form_layout.addRow(self.upload_video_label, self.upload_video_button)
        video_upload_form_layout.addRow(self.set_datetime_label, self.set_datetime_input)
        video_upload_form_layout.addRow(self.choose_store_label, self.choose_store_input)
        video_upload_form_layout.addRow(self.heatmap_label, self.heatmap_checkbox)
        
        self.process_video_button = QPushButton('Process Video')
        self.process_video_button.setObjectName("process_video_button")
        self.process_video_button.clicked.connect(self.handle_process_video)
        
        video_layout.addWidget(self.video_label)
        video_layout.addWidget(self.video_upload_description)
        video_layout.addLayout(video_upload_form_layout)
        video_layout.addWidget(self.process_video_button, alignment=Qt.AlignCenter)
        
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
            self.upload_video_button.setText(file_name)
            self.file_name = file_name

    def is_empty(self, value):
      return len(value) == 0

    def handle_process_video(self):
        self.store_name = self.choose_store_input.currentText()
        self.store_id = self.storeIds[self.store_name]
        if self.is_empty(self.file_name) or self.is_empty(self.user) or self.is_empty(self.store_name):
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Error")
            error_message.setText("Please fill in all the fields")
            error_message.exec_()
        else:

            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker(self.user, self.file_name, self.choose_store_input.currentText(), self.store_id,
                                 self.set_datetime_input.dateTime().toPyDateTime(), self.heatmap_checkbox.isChecked())
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # Step 6: Start the thread
            self.thread.start()
            self.spinner_dialog = SpinnerDialog(f"Video is processing ...")
            self.spinner_dialog.show()

            # Final resets
            self.thread.finished.connect( lambda: self.spinner_dialog.accept() )
            
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, user, file_name, store_name, store_id, date_time, heatmap_checked):
        QObject.__init__(self)
        self.user = user
        self.file_name = file_name
        self.store_name = store_name
        self.store_id = store_id
        self.date_time = date_time
        self.heatmap_checked = heatmap_checked

    def run(self):
        computer_vision.process_video(self.file_name, 10, self.user, self.store_name, self.store_id, self.date_time, self.heatmap_checked)
        self.finished.emit()