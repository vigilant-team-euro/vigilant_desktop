import sys
from PyQt5.QtWidgets import *

from pages.login_page import LoginScreen
from pages.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application icon
    #app.setWindowIcon(QIcon('images/logo.png'))

    login_screen = LoginScreen()
    if login_screen.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec_())
