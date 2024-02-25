from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDateTime

class CameraPage(QWidget):
    
   def __init__(self):
      super().__init__()

      self.initUI()

   def initUI(self):
      camera_layout = QVBoxLayout()
      
      self.camera_label = QLabel('IP Camera Adding & Footage Processing')
      self.camera_label.setObjectName("camera_label")
      self.camera_label.setAlignment(Qt.AlignHCenter)
      self.camera_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
   
      tabs = QTabWidget()
      tabs.addTab(self.add_camera_tab(), "Add Camera")
      tabs.addTab(self.delete_camera_tab(), "Delete Camera")
      tabs.addTab(self.process_camera_footage_tab(), "Process Camera Footage")
      
      camera_layout.addWidget(self.camera_label)
      camera_layout.addWidget(tabs, alignment=Qt.AlignHCenter)
      
      self.setLayout(camera_layout)
      
      with open('styles/camera_styles.qss', 'r') as style_file:
         self.setStyleSheet(style_file.read())
        
   def add_camera_tab(self):
      INPUT_WIDTH = 300
      
      add_camera_tab = QWidget()
      add_camera_layout = QVBoxLayout()
      
      self.add_camera_label = QLabel('Please fill in the details of the camera you want to add.')
      self.add_camera_label.setObjectName("add_camera_label")
      self.add_camera_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
      
      add_camera_form_layout = QFormLayout()
      add_camera_form_layout.setSpacing(40)
      
      self.camera_name_input = QLineEdit()
      self.camera_name_label = QLabel('Camera Name')
      self.camera_name_label.setObjectName("camera_name_label")
      self.camera_name_input.setFixedWidth(INPUT_WIDTH)
      self.camera_name_input.setPlaceholderText('Enter camera name')
      
      self.camera_ip_input = QLineEdit()
      self.camera_ip_label = QLabel('Camera IP')
      self.camera_ip_label.setObjectName("camera_ip_label")
      self.camera_ip_input.setFixedWidth(INPUT_WIDTH)
      self.camera_ip_input.setPlaceholderText('Enter camera IP')
      
      self.camera_port_input = QLineEdit()
      self.camera_port_label = QLabel('Camera Port')
      self.camera_port_label.setObjectName("camera_port_label")
      self.camera_port_input.setFixedWidth(INPUT_WIDTH)
      self.camera_port_input.setPlaceholderText('Enter camera port')
      
      self.camera_username_input = QLineEdit()
      self.camera_username_label = QLabel('Camera Username')
      self.camera_username_label.setObjectName("camera_username_label")
      self.camera_username_input.setFixedWidth(INPUT_WIDTH)
      self.camera_username_input.setPlaceholderText('Enter camera username')
      
      self.camera_password_input = QLineEdit()
      self.camera_password_label = QLabel('Camera Password')
      self.camera_password_label.setObjectName("camera_password_label")
      self.camera_password_input.setFixedWidth(INPUT_WIDTH)
      self.camera_password_input.setPlaceholderText('Enter camera password')
      self.camera_password_input.setEchoMode(QLineEdit.Password)
      
      self.store_name_combobox = QComboBox()
      self.store_name_label = QLabel('Store Name')
      self.store_name_label.setObjectName("store_name_label")
      self.store_name_combobox.setFixedWidth(INPUT_WIDTH)
      self.store_name_combobox.setPlaceholderText('Choose store name')
      
      add_camera_form_layout.addRow(self.camera_name_label, self.camera_name_input)
      add_camera_form_layout.addRow(self.camera_ip_label, self.camera_ip_input)
      add_camera_form_layout.addRow(self.camera_port_label, self.camera_port_input)
      add_camera_form_layout.addRow(self.camera_username_label, self.camera_username_input)
      add_camera_form_layout.addRow(self.camera_password_label, self.camera_password_input)
      add_camera_form_layout.addRow(self.store_name_label, self.store_name_combobox)
      
      self.add_camera_button = QPushButton('Add Camera')
      self.add_camera_button.setObjectName("add_camera_button")
      #self.setFixedWidth(600)
      
      add_camera_layout.addWidget(self.add_camera_label)
      add_camera_layout.addLayout(add_camera_form_layout)
      add_camera_layout.addWidget(self.add_camera_button, alignment=Qt.AlignCenter)
      
      add_camera_tab.setLayout(add_camera_layout)
      
      return add_camera_tab
   
   def delete_camera_tab(self):
      INPUT_WIDTH = 250
      delete_camera_tab = QWidget()
      delete_camera_layout = QVBoxLayout()
      
      self.delete_camera_label = QLabel('Please choose the camera you want to delete.')
      self.delete_camera_label.setObjectName("delete_camera_label")
      self.delete_camera_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
      
      delete_camera_form_layout = QFormLayout()
      delete_camera_form_layout.setSpacing(60)
      
      self.choose_delete_camera_label = QLabel('Choose Camera')
      self.choose_delete_camera_label.setObjectName("choose_delete_camera_label")
      self.choose_delete_camera_input = QComboBox()
      self.choose_delete_camera_input.setFixedWidth(INPUT_WIDTH)
      self.choose_delete_camera_input.setPlaceholderText('Choose camera')
      
      delete_camera_form_layout.addRow(self.choose_delete_camera_label, self.choose_delete_camera_input)
      
      self.delete_camera_button = QPushButton('Delete Camera')
      self.delete_camera_button.setObjectName("delete_camera_button")
      
      delete_camera_layout.addWidget(self.delete_camera_label)
      delete_camera_layout.addLayout(delete_camera_form_layout)
      delete_camera_layout.addWidget(self.delete_camera_button, alignment=Qt.AlignCenter)
      
      delete_camera_tab.setLayout(delete_camera_layout)
      
      return delete_camera_tab
   
   def process_camera_footage_tab(self):
      INPUT_WIDTH = 250
      process_camera_footage_tab = QWidget()
      process_camera_footage_layout = QVBoxLayout()
      
      self.process_description_label = QLabel('Please choose the store and camera you want to process the footage for.')
      self.process_description_label.setObjectName("process_description_label")
      self.process_description_label.setObjectName("process_description_label")
      self.process_description_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
      
      process_camera_footage_form_layout = QFormLayout()
      process_camera_footage_form_layout.setSpacing(60)
      
      self.choose_store_label = QLabel('Choose Store')
      self.choose_store_label.setObjectName("choose_store_label")
      self.choose_store_input = QComboBox()
      self.choose_store_input.setFixedWidth(INPUT_WIDTH)
      self.choose_store_input.setPlaceholderText('Choose store')
      
      self.choose_camera_label = QLabel('Choose Camera')
      self.choose_camera_label.setObjectName("choose_camera_label")
      self.choose_camera_input = QComboBox()
      self.choose_camera_input.setFixedWidth(INPUT_WIDTH)
      self.choose_camera_input.setPlaceholderText('Choose camera')
      
      self.set_datetime_label = QLabel('Set Date and Time')
      self.set_datetime_label.setObjectName("set_datetime_label")
      self.set_datetime_input = QDateTimeEdit()
      self.set_datetime_input.setFixedWidth(INPUT_WIDTH)
      self.set_datetime_input.setDateTime(QDateTime.currentDateTime())
      
      process_camera_footage_form_layout.addRow(self.choose_store_label, self.choose_store_input)
      process_camera_footage_form_layout.addRow(self.choose_camera_label, self.choose_camera_input)
      process_camera_footage_form_layout.addRow(self.set_datetime_label, self.set_datetime_input)
      
      self.start_process_button = QPushButton('Start Process')
      self.start_process_button.setObjectName("start_process_button")
      
      process_camera_footage_layout.addWidget(self.process_description_label)
      process_camera_footage_layout.addLayout(process_camera_footage_form_layout)
      process_camera_footage_layout.addWidget(self.start_process_button, alignment=Qt.AlignCenter)
      
      process_camera_footage_tab.setLayout(process_camera_footage_layout)
      
      return process_camera_footage_tab