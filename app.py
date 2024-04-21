import sys
from PyQt5.QtWidgets import *

from pages.login_page import LoginScreen
from pages.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_screen = LoginScreen()
    if login_screen.exec_() == QDialog.Accepted:
        user_info = login_screen.getUserInfo()
        main_window = MainWindow(user_info=user_info)
        main_window.show()

    sys.exit(app.exec_())
