import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
import utils
# Import the style file

class LoginScreen(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit(self)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Apply style to the login screen
        with open('styles.qss', 'r') as style_file:
            self.setStyleSheet(style_file.read())

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Add your authentication logic here
        if utils.auth_user(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')
class CameraPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel('Camera Page')
        layout.addWidget(label)
        self.setLayout(layout)

class EmployeePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel('Employee Page')
        layout.addWidget(label)
        self.setLayout(layout)

class StorePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel('Store Page')
        layout.addWidget(label)
        self.setLayout(layout)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(300, 300, 500, 300)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Add other menu items and functionalities as needed
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.camera_page = CameraPage()
        self.employee_page = EmployeePage()
        self.store_page = StorePage()

        self.stacked_widget.addWidget(self.camera_page)
        self.stacked_widget.addWidget(self.employee_page)
        self.stacked_widget.addWidget(self.store_page)
        self.stacked_widget.setCurrentWidget(self.camera_page)

        # Create actions to switch between pages
        camera_action = QAction('Camera Page', self)
        camera_action.triggered.connect(lambda: self.switch_page(self.camera_page))

        employee_action = QAction('Employee Page', self)
        employee_action.triggered.connect(lambda: self.switch_page(self.employee_page))

        store_action = QAction('Store Page', self)
        store_action.triggered.connect(lambda: self.switch_page(self.store_page))

        menubar.addAction(camera_action)
        menubar.addAction(employee_action)
        menubar.addAction(store_action)

    def logout(self):
        login_screen = LoginScreen()
        if login_screen.exec_() == QDialog.Accepted:
            self.show()
    def switch_page(self, page):
        self.stacked_widget.setCurrentWidget(page)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application icon
    app.setWindowIcon(QIcon('icon.png'))  # Replace 'icon.png' with your icon file

    login_screen = LoginScreen()
    if login_screen.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec_())
