from PyQt5.QtWidgets import *
from pages.login_page import LoginScreen
from pages.camera_page import CameraPage
from pages.video_page import VideoPage
from pages.main_page import MainPage

class MainWindow(QMainWindow):
   def __init__(self, user_info):
      super().__init__()
      self.user_info = user_info
      self.init_ui()

   def init_ui(self):
      self.setWindowTitle('Vigilant Desktop Application')
      self.setGeometry(300, 300, 1350, 900)

      menubar = self.menuBar()

      self.center_on_screen()
      
      self.stacked_widget = QStackedWidget(self)
      self.setCentralWidget(self.stacked_widget)
      self.main_page = MainPage(user_info=self.user_info)
      self.camera_page = CameraPage(user_info=self.user_info)
      self.video_page = VideoPage(user_info=self.user_info)

      self.stacked_widget.addWidget(self.main_page)
      self.stacked_widget.addWidget(self.camera_page)
      self.stacked_widget.addWidget(self.video_page)
      self.stacked_widget.setCurrentWidget(self.main_page)

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
      logout_action.triggered.connect(self.logout)
          
      file_menu.addAction(logout_action)
      
      with open('styles/main_window_styles.qss', 'r') as style_file:
         self.setStyleSheet(style_file.read())

   def center_on_screen(self):
      screen_geometry = QDesktopWidget().screenGeometry()

      x = (screen_geometry.width() - self.width()) // 2
      y = (screen_geometry.height() - self.height()) // 2

      self.move(x, y)

   def logout(self):
      self.close()
      login_screen = LoginScreen()
      login_screen.exec_()

   def switch_page(self, page):
      self.stacked_widget.setCurrentWidget(page)
