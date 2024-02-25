from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class EmployeePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        INPUT_WIDTH = 300
        layout = QVBoxLayout()
        
        employee_frame = QFrame()
        employee_layout = QVBoxLayout()
        
        self.employee_label = QLabel('Employee Registeration')
        self.employee_label.setObjectName("employee_label")
        self.employee_label.setAlignment(Qt.AlignHCenter)
        self.employee_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        layout.addWidget(self.employee_label, alignment=Qt.AlignHCenter)
        
        employee_upload_form_layout = QFormLayout()
        employee_upload_form_layout.setSpacing(40)
        
        self.employee_upload_description = QLabel('Please register the employee by uploading their portait.')
        self.employee_upload_description.setObjectName("employee_upload_description")
        self.employee_upload_description.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        self.employee_name_label = QLabel('Name')
        self.employee_name_label.setObjectName("employee_name_label")
        self.employee_name_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.employee_name_input = QLineEdit()
        self.employee_name_input.setPlaceholderText('Enter employee name')
        self.employee_name_input.setFixedWidth(INPUT_WIDTH)
        
        self.employee_surname_label = QLabel('Surname')
        self.employee_surname_label.setObjectName("employee_surname_label")
        self.employee_surname_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.employee_surname_input = QLineEdit()
        self.employee_surname_input.setPlaceholderText('Enter employee surname')
        self.employee_surname_input.setFixedWidth(INPUT_WIDTH)
        
        self.upload_employee_image_label = QLabel('Upload Image of Employee')
        self.upload_employee_image_label.setObjectName("upload_employee_image_label")
        self.upload_employee_image_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.upload_employee_image_button = QPushButton('Upload Image of Employee')
        self.upload_employee_image_button.setObjectName("upload_employee_image_button")
        self.upload_employee_image_button.clicked.connect(self.upload_image)
        
        employee_upload_form_layout.addRow(self.employee_name_label, self.employee_name_input)
        employee_upload_form_layout.addRow(self.employee_surname_label, self.employee_surname_input)
        employee_upload_form_layout.addRow(self.upload_employee_image_label, self.upload_employee_image_button)
        
        register_employee_button = QPushButton('Register Employee')
        register_employee_button.setObjectName("register_employee_button")
        
        employee_layout.addWidget(self.employee_label)
        employee_layout.addWidget(self.employee_upload_description)
        employee_layout.addLayout(employee_upload_form_layout)
        employee_layout.addWidget(register_employee_button, alignment=Qt.AlignCenter)
        
        employee_frame.setLayout(employee_layout)
        
        layout.addWidget(employee_frame, alignment=Qt.AlignHCenter)
        self.setLayout(layout)
        
        with open('styles/employee_styles.qss', 'r') as style_file:
            self.setStyleSheet(style_file.read())
        
        
    def upload_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)", options=options)
        if file_name:
            print("Uploaded image:", file_name)