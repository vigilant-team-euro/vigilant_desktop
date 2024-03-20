from PyQt5.QtWidgets import *
from pages.login_page import LoginScreen
from pages.camera_page import CameraPage
from pages.video_page import VideoPage
from pages.main_page import MainPage
import utils

class MainWindow(QMainWindow):
   def __init__(self, user):
      super().__init__()
      self.user = user
      self.init_ui()

   def init_ui(self):
      self.setWindowTitle('Main Window')
      self.setGeometry(300, 300, 1350, 900)
      #self.setMinimumWidth(1300)

      menubar = self.menuBar()

      self.center_on_screen()
      # Add other menu items and functionalities as needed
      self.stacked_widget = QStackedWidget(self)
      self.setCentralWidget(self.stacked_widget)
      self.main_page = MainPage(user=self.user)
      self.camera_page = CameraPage(user=self.user)
      self.video_page = VideoPage(user=self.user)

      self.stacked_widget.addWidget(self.main_page)
      self.stacked_widget.addWidget(self.camera_page)
      self.stacked_widget.addWidget(self.video_page)
      self.stacked_widget.setCurrentWidget(self.main_page)

      # Create actions to switch between pages
      main_action = QAction('Main Page', self)
      main_action.triggered.connect(lambda: self.switch_page(self.main_page))

      camera_action = QAction('Camera Page', self)
      camera_action.triggered.connect(lambda: self.switch_page(self.camera_page))
      
      video_action = QAction('Video Page', self)
      video_action.triggered.connect(lambda: self.switch_page(self.video_page))

      menubar.addAction(main_action)
      menubar.addAction(camera_action)
      menubar.addAction(video_action)
      
      file_menu = menubar.addMenu('Logout')

      logout_action = QAction('Logout', self)

      if utils.is_user_logged_out():
          logout_action.triggered.connect(self.close)
          
      file_menu.addAction(logout_action)
      
      with open('styles/main_window_styles.qss', 'r') as style_file:
         self.setStyleSheet(style_file.read())

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
