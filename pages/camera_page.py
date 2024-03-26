from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDateTime, QThread, QObject, pyqtSignal
import utils
import ipaddress
from components.spinner import SpinnerDialog
import firebase
import computer_vision

TABLE_HORIZONTAL_HEADERS = ["Camera Name", "IP Address", "Store", "Footage", "Delete"]

class CameraPage(QWidget):
    
   def __init__(self, user):
      super().__init__()
      self.ip_addresses = []
      self.user = user
      self.initUI()

   def initUI(self):
      camera_layout = QVBoxLayout()
      
      self.camera_label = QLabel('IP Camera Adding & Footage Processing')
      self.camera_label.setObjectName("camera_label")
      self.camera_label.setAlignment(Qt.AlignHCenter)
      self.camera_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
   
      self.tabs = QTabWidget()
      
      self.tabs.addTab(self.available_cameras_tab(), "Available Cameras")
      self.tabs.addTab(self.add_camera_tab(), "Add Camera")
      self.tabs.addTab(self.process_camera_footage_tab(), "Process Camera Footage")
      camera_layout.addWidget(self.camera_label)
      camera_layout.addWidget(self.tabs, alignment=Qt.AlignHCenter)
      
      self.setLayout(camera_layout)
      
      with open('styles/camera_styles.qss', 'r') as style_file:
         self.setStyleSheet(style_file.read())
   
   def available_cameras_tab(self):
      
      registered_cameras_tab = QWidget()
      registered_cameras_layout = QVBoxLayout()
      
      self.registered_cameras_label = QLabel('Registered Cameras')
      self.registered_cameras_label.setObjectName("registered_cameras_label")
      self.registered_cameras_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
      
      self.table = QTableWidget()
      self.table.setColumnCount(5)
      self.table.itemChanged.connect(self.handle_table_item_changed)
      
      self.update_camera_table()
      
      header = self.table.horizontalHeader()
      header.setDefaultSectionSize(self.tabs.size().width() // 5)  # Adjust column thickness
      header = self.table.verticalHeader()
      header.setDefaultSectionSize(50)   # Adjust row thickness

      registered_cameras_layout.addWidget(self.registered_cameras_label)
      registered_cameras_layout.addWidget(self.table)

      registered_cameras_tab.setLayout(registered_cameras_layout)
      
      return registered_cameras_tab
       
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
      self.store_name_combobox.addItems(firebase.getStoreNames(self.user))
      
      add_camera_form_layout.addRow(self.camera_name_label, self.camera_name_input)
      add_camera_form_layout.addRow(self.camera_ip_label, self.camera_ip_input)
      add_camera_form_layout.addRow(self.camera_port_label, self.camera_port_input)
      add_camera_form_layout.addRow(self.camera_username_label, self.camera_username_input)
      add_camera_form_layout.addRow(self.camera_password_label, self.camera_password_input)
      add_camera_form_layout.addRow(self.store_name_label, self.store_name_combobox)
      
      self.add_camera_button = QPushButton('Add Camera')
      self.add_camera_button.setObjectName("add_camera_button")
      self.add_camera_button.clicked.connect(self.handle_add_camera)
      #self.setFixedWidth(600)
      
      add_camera_layout.addWidget(self.add_camera_label)
      add_camera_layout.addLayout(add_camera_form_layout)
      add_camera_layout.addWidget(self.add_camera_button, alignment=Qt.AlignCenter)
      
      add_camera_tab.setLayout(add_camera_layout)
      
      return add_camera_tab
   
   def process_camera_footage_tab(self):
      INPUT_WIDTH = 250
      process_camera_footage_tab = QWidget()
      process_camera_footage_layout = QVBoxLayout()
      
      self.process_description_label = QLabel('Please choose the store and camera you want to process the footage for.')
      self.process_description_label.setObjectName("process_description_label")
      self.process_description_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
      
      process_camera_footage_form_layout = QFormLayout()
      process_camera_footage_form_layout.setSpacing(60)
      
      self.choose_camera_label = QLabel('Choose Camera')
      self.choose_camera_label.setObjectName("choose_camera_label")
      self.choose_camera_input = QComboBox()
      self.choose_camera_input.setFixedWidth(INPUT_WIDTH)
      self.choose_camera_input.setPlaceholderText('Choose camera')

      self.choose_store_label = QLabel('Choose Store')
      self.choose_store_label.setObjectName("choose_store_label")
      self.choose_store_input = QComboBox()
      self.choose_store_input.setFixedWidth(INPUT_WIDTH)
      self.choose_store_input.setPlaceholderText('Choose store')
      self.choose_store_input.addItems(firebase.getStoreNames(self.user))
      self.choose_store_input.currentTextChanged.connect(self.update_camera_combobox)
      
      self.heatmap_label = QLabel('Generate Heatmap')
      self.heatmap_label.setObjectName("heatmap_label")
      
      self.heatmap_checkbox = QCheckBox()
      self.heatmap_checkbox.setObjectName("heatmap_checkbox")
      self.heatmap_checkbox.setChecked(True)
      
      process_camera_footage_form_layout.addRow(self.choose_store_label, self.choose_store_input)
      process_camera_footage_form_layout.addRow(self.choose_camera_label, self.choose_camera_input)
      process_camera_footage_form_layout.addRow(self.heatmap_label, self.heatmap_checkbox)
      
      self.start_process_button = QPushButton('Start Process')
      self.start_process_button.setObjectName("start_process_button")
      self.start_process_button.clicked.connect(self.handle_start_process)
      
      process_camera_footage_layout.addWidget(self.process_description_label)
      process_camera_footage_layout.addLayout(process_camera_footage_form_layout)
      process_camera_footage_layout.addWidget(self.start_process_button, alignment=Qt.AlignCenter)
      
      process_camera_footage_tab.setLayout(process_camera_footage_layout)
      
      return process_camera_footage_tab
   
   # UI Functionality
   def handle_add_camera(self):
      error_message = QMessageBox()
      error_message.setIcon(QMessageBox.Critical)
      error_message.setWindowTitle("Error")
      
      camera_name = self.camera_name_input.text().strip()
      camera_ip = self.camera_ip_input.text().strip()
      camera_port = self.camera_port_input.text().strip()
      camera_username = self.camera_username_input.text().strip()
      camera_password = self.camera_password_input.text().strip()
      store_name = "store_name" # CHANGE THIS WHEN THE FIREBASE INTEGRATION IS DONE
      
      if self.is_empty(camera_name) or self.is_empty(camera_ip) or self.is_empty(camera_port) or self.is_empty(camera_username) or self.is_empty(camera_password):
         error_message.setText("Please fill in all the fields")
         error_message.exec_()
         return
      
      if not self.validate_ip_address(camera_ip):
         error_message.setText("Please enter a valid IP address!")
         error_message.exec_()
         self.camera_ip_input.clear()
         return
      
      if not self.validate_port_number(camera_port):
         error_message.setText("Please enter a valid port number!")
         error_message.exec_()
         self.camera_port_input.clear()
         return
      
      camera_port = int(camera_port)
      
      # DB Operation
      db_error = utils.add_camera(camera_name, camera_ip, camera_port, camera_username, camera_password, store_name)
      
      if len(db_error) > 0:
         error_message.setText(db_error)
         error_message.exec_()
         self.camera_name_input.clear()
         self.camera_username_input.clear()
         self.camera_password_input.clear()
         #self.store_name_combobox.setCurrentIndex(0)
         return

      success_message = QMessageBox()
      success_message.setIcon(QMessageBox.Information)
      success_message.setWindowTitle("Success")
      success_message.setText("Camera added successfully!")
      success_message.exec_()
      
      # Reload the page
      self.update_camera_table()
      
   def handle_delete_camera(self, deleted_camera_name):
      error = utils.remove_camera(deleted_camera_name)
      
      if len(error) > 0:
         error_message = QMessageBox()
         error_message.setIcon(QMessageBox.Critical)
         error_message.setWindowTitle("Error")
         error_message.setText("Failed to delete camera")
         error_message.exec_()
         return
      
      self.update_camera_table()
      
      success_message = QMessageBox()
      success_message.setIcon(QMessageBox.Information)
      success_message.setWindowTitle("Success")
      success_message.setText("Camera added successfully!")
      success_message.exec_()
      
   def handle_show_live_footage(self, camera_name):
      
      self.thread = self.LiveFootageThread(camera_name)
      self.thread.finished.connect(self.on_live_footage_finished)
      
      self.spinner_dialog = SpinnerDialog(f"Connecting to {camera_name}...")
      self.spinner_dialog.show()
    
      self.thread.start()
      
   def on_live_footage_finished(self, error):
      self.spinner_dialog.accept()
      self.spinner_dialog = None
      
      # Check if there was an error
      if len(error) > 0:
         error_message = QMessageBox()
         error_message.setIcon(QMessageBox.Critical)
         error_message.setWindowTitle("Error")
         error_message.setText(error)
         error_message.exec_()
      
      # Clean up the thread
      self.thread.deleteLater()
      self.thread = None
   
   def handle_table_item_changed(self, item):
      if item.column() == 1: # IP Address column
         if not self.validate_ip_address(item.text()):
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Error")
            error_message.setText("Please enter a valid IP address!")
            error_message.exec_()
            item.setText(self.ip_addresses[item.row()])
         else:
            camera_name = self.table.item(item.row(), 0).text()
            utils.edit_camera_ip(camera_name, item.text())
            
   def handle_start_process(self):
      if self.choose_camera_input.currentText() == None or self.choose_store_input.currentText() == None:
         error_message = QMessageBox()
         error_message.setIcon(QMessageBox.Critical)
         error_message.setWindowTitle("Error")
         error_message.setText("Please fill in all the fields")
         error_message.exec_()
         return
      else:
         camera_name = self.choose_camera_input.currentText()
         store_name = self.choose_store_input.currentText()
         heatmap_generation = self.heatmap_checkbox.isChecked()
         
         self.thread = QThread()
         self.worker = Worker(self.user, camera_name, store_name, heatmap_generation)
         self.worker.moveToThread(self.thread)
         self.thread.started.connect(self.worker.run)
         self.worker.finished.connect(self.thread.quit)
         self.worker.finished.connect(self.worker.deleteLater)
         self.thread.finished.connect(self.thread.deleteLater)
         self.thread.start()
         self.spinner_dialog = SpinnerDialog(f"Processing footage for {camera_name} ...")
         self.spinner_dialog.show()
         self.thread.finished.connect( lambda: self.spinner_dialog.accept() )

   # HELPER FUNCTIONS
   def update_camera_table(self):
      cameras = utils.get_cameras()
      cameras_dict = []
      self.ip_addresses = []
      
      for camera in cameras:
         cameras_dict.append({"name": camera[0], "ip_address": camera[1], "store": camera[2]})
      
      self.table.setRowCount(len(cameras_dict))
      self.table.setHorizontalHeaderLabels(TABLE_HORIZONTAL_HEADERS)
      
      for index in range(len(cameras_dict)):
         camera = cameras_dict[index]
         self.table.setItem(index, 0, QTableWidgetItem(camera["name"]))
         self.table.setItem(index, 1, QTableWidgetItem(camera["ip_address"]))
         self.table.setItem(index, 2, QTableWidgetItem(camera["store"]))
         footage_btn = QPushButton('Live Footage')
         footage_btn.setStyleSheet("background-color: darkblue; color: white")
         self.table.setCellWidget(index, 3, footage_btn)
         footage_btn.clicked.connect(lambda checked, cam=camera: self.handle_show_live_footage(cam["name"]))
         delete_btn = QPushButton('Delete')
         delete_btn.setStyleSheet("background-color: darkred; color: white")
         self.table.setCellWidget(index, 4, delete_btn)
         delete_btn.clicked.connect(lambda checked, cam=camera: self.handle_delete_camera(cam["name"]))
         
         self.ip_addresses.append(camera["ip_address"])
      
      self.set_column_read_only(self.table, 0) # Make the camera name column read-only
      self.set_column_read_only(self.table, 2)  # Make the store name column read-only

   def is_empty(self, value):
      return len(value) == 0
   
   def validate_port_number(self, port_number):
      try:
         port = int(port_number)
         return port > 0 and port < 65536
      except ValueError:
         return False
      
   def validate_ip_address(self, ip_address):
      try:
         ipaddress.ip_address(ip_address)
         return True
      except ValueError:
         return False
   
   def set_column_read_only(self, table_widget, column_index):
      for row_index in range(table_widget.rowCount()):
         item = table_widget.item(row_index, column_index)
         if item is not None:
            # Remove the ItemIsEditable flag to make the item read-only
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
         else:
            # If the cell is empty, create a new non-editable item
            non_editable_item = QTableWidgetItem()
            non_editable_item.setFlags(non_editable_item.flags() & ~Qt.ItemIsEditable)
            table_widget.setItem(row_index, column_index, non_editable_item)
   
   def update_camera_combobox(self):
      self.choose_camera_input.clear()
      store_name = self.choose_store_input.currentText()
      if store_name != None:
         self.choose_camera_input.addItems(utils.get_store_cameras(store_name))

   # Threads
   class LiveFootageThread(QThread):
      
      finished = pyqtSignal(str)

      def __init__(self, camera_name):
         super().__init__()
         self.camera_name = camera_name

      def run(self):
         error = utils.show_live_footage(self.camera_name)
         self.finished.emit(error)
   
class Worker(QObject):
   finished = pyqtSignal()
   progress = pyqtSignal(int)

   def __init__(self, user, camera_name, store_name, heatmap_checked):
      QObject.__init__(self)
      self.user = user
      self.camera_name = camera_name
      self.store_name = store_name
      self.heatmap_checked = heatmap_checked

   def run(self):
      rtsp_url = utils.construct_rtsp_url(self.camera_name)
      computer_vision.process_live_camera_footage(rtsp_url, 30, self.user, self.store_name, QDateTime.currentDateTime().toPyDateTime(), self.heatmap_checked)
      self.finished.emit()