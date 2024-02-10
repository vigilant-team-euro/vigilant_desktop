import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import utils
# Import the style file

class LoginScreen(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 150)
        self.center_on_screen()
        layout = QVBoxLayout()
        
        self.vigilant_label = QLabel('Vigilant')
        self.vigilant_label.setStyleSheet("font-size: 30pt; color: blue; font-weight: bold;")
        self.vigilant_label.setAlignment(Qt.AlignHCenter)

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit(self)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(self.vigilant_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Apply style to the login screen
        with open('styles.qss', 'r') as style_file:
            self.setStyleSheet(style_file.read())
            
        self.rejected.connect(sys.exit)
            
    def center_on_screen(self):
        # Get the screen geometry
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate the center of the screen
        x = (screen_geometry.width() - self.width()) // 2
        y = ((screen_geometry.height() - self.height()) // 5) * 2

        # Set the position of the main window
        self.move(x, y)

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
        self.setObjectName("CameraPage")
        layout = QVBoxLayout()
        label = QLabel('Camera Page')
        layout.addWidget(label)
        self.setLayout(layout)

class EmployeePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setObjectName("EmployeePage")
        layout = QVBoxLayout()
        label = QLabel('Employee Page')
        layout.addWidget(label)
        self.setLayout(layout)

class StorePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setObjectName("StorePage")
        layout = QVBoxLayout()
        label = QLabel('Store Page')
        layout.addWidget(label)
        self.setLayout(layout)

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setObjectName("MainPage")
        layout = QVBoxLayout()
        label = QLabel('Main Page')
        layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(300, 300, 1200, 900)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('Logout')

        logout_action = QAction('Logout', self)

        if utils.is_user_logged_out():
            logout_action.triggered.connect(self.close)
        file_menu.addAction(logout_action)

        self.center_on_screen()
        # Add other menu items and functionalities as needed
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.main_page = MainPage()
        self.camera_page = CameraPage()
        self.employee_page = EmployeePage()
        self.store_page = StorePage()

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.camera_page)
        self.stacked_widget.addWidget(self.employee_page)
        self.stacked_widget.addWidget(self.store_page)
        self.stacked_widget.setCurrentWidget(self.camera_page)

        # Create actions to switch between pages
        main_action = QAction('Main Page', self)
        main_action.triggered.connect(lambda: self.switch_page(self.main_page))

        camera_action = QAction('Camera Page', self)
        camera_action.triggered.connect(lambda: self.switch_page(self.camera_page))

        employee_action = QAction('Employee Page', self)
        employee_action.triggered.connect(lambda: self.switch_page(self.employee_page))

        store_action = QAction('Store Page', self)
        store_action.triggered.connect(lambda: self.switch_page(self.store_page))

        menubar.addAction(main_action)
        menubar.addAction(camera_action)
        menubar.addAction(employee_action)
        menubar.addAction(store_action)

    def center_on_screen(self):
        # Get the screen geometry
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate the center of the screen
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Set the position of the main window
        self.move(x, y)

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
