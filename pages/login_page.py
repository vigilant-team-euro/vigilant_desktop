import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import utils

login_image_path = 'images/shopView.jpeg'
login_screen_x = 300
login_screen_y = 300
login_screen_width = 400
login_screen_height = 150

class LoginScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.user = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Vigilant Desktop Application')
        self.setGeometry(login_screen_x, login_screen_y, login_screen_width, login_screen_height)
        self.center_on_screen()
        
        main_layout = QHBoxLayout()
        
        pixmap = QPixmap(login_image_path)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        main_layout.addWidget(label)
        label.setMinimumSize(600, login_screen_height)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        login_layout = QVBoxLayout()
        
        vigilant_pixmap = QPixmap('images/vigilant_logo.png')
        self.vigilant_label = QLabel()
        self.vigilant_label.setPixmap(vigilant_pixmap)
        #self.vigilant_label.setObjectName("vigilant_label")
        self.vigilant_label.setAlignment(Qt.AlignHCenter)
        
        self.description_label = QLabel('Welcome to Vigilant Desktop Application!\nPlease login to continue.')
        self.description_label.setObjectName("description_label")
        self.description_label.setAlignment(Qt.AlignHCenter)

        email_layout = QVBoxLayout()
        self.email_label = QLabel('Email')
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Enter your email')
        email_layout.addWidget(self.email_label)
        email_layout.addWidget(self.email_input)
        
        password_layout = QVBoxLayout()
        self.password_label = QLabel('Password')
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.setObjectName("login_button")
        self.login_button.clicked.connect(self.handle_login)
        
        self.google_button = QPushButton("Sign in with Google", self)
        self.google_button.setObjectName("google_button")
        google_icon = QIcon("icons/google_icon.png")  # Replace with the path to your Google icon
        self.google_button.setIcon(google_icon)
        self.google_button.clicked.connect(self.handle_google_login)
        #self.google_button.setIconSize(google_icon.actualSize(self.google_button.size()))

        login_layout.addWidget(self.vigilant_label)
        login_layout.addWidget(self.description_label)
        login_layout.addLayout(email_layout)
        login_layout.addLayout(password_layout)
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.google_button)

        main_layout.addLayout(login_layout)
        
        self.setLayout(main_layout)

        # Apply style to the login screen
        with open('styles/login_styles.qss', 'r') as style_file:
            self.setStyleSheet(style_file.read())
        
        self.rejected.connect(sys.exit)
            
    def center_on_screen(self):
        # Get the screen geometry
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate the center of the screen
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Set the position of the main window
        self.move(x, y)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if email == "" or password == "":
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Warning)
            error_message.setWindowTitle("Login Failed")
            error_message.setText("Please enter your email and password!")
            error_message.exec_()
            return
        
        user_info = utils.auth_user(email, password)
        # Add your authentication logic here
        if user_info['user'] != "":
            self.user_info = user_info
            self.accept()
        else:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Login Failed")
            error_message.setText("Invalid email or password")
            error_message.exec_()
            return

    def handle_google_login(self):
        if utils.auth_user_google():
            self.accept
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid email or password')

    def getUserInfo(self):
        return self.user_info