import sys
from PyQt5.QtWidgets import *

from pages.login_page import LoginScreen
from pages.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_screen = LoginScreen()
    if login_screen.exec_() == QDialog.Accepted:
        user = login_screen.getUser()
        main_window = MainWindow(user=user)
        main_window.show()

    sys.exit(app.exec_())
