import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import utils
from pages.login_page import LoginScreen

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