from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

main_image_path = 'images/mainPage.jpeg'
heatmap_image_path = 'images/heatmap.png'
emotion_image_path = 'images/emotion.jpeg'

class MainPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        
        main_pixmap = QPixmap(main_image_path)
        label = QLabel()
        label.setPixmap(main_pixmap)
        label.setScaledContents(True)
        
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setMinimumSize(900, 400)
        label.setMaximumSize(100000, 400)
        
        main_layout.addWidget(label)
        label.setAlignment(Qt.AlignCenter)
        
        overview_layout = QHBoxLayout()

        # Heatmap Description
        heatmap_frame = QFrame()
        heatmap_frame.setFrameShape(QFrame.StyledPanel)
        heatmap_frame.setFrameShadow(QFrame.Raised)
        heatmap_frame.setFixedSize(400, 500)
        
        heatmap_layout = QVBoxLayout(heatmap_frame)
        
        heatmap_pixmap = QPixmap(heatmap_image_path)
        heatmap_label = QLabel()
        heatmap_label.setObjectName("heatmap_label")
        heatmap_label.setPixmap(heatmap_pixmap)
        heatmap_label.setScaledContents(True)
        
        heatmap_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        heatmap_label.setMinimumSize(300, 300)
        heatmap_label.setMaximumSize(300, 300)
        heatmap_label.setAlignment(Qt.AlignCenter)
        
        self.heatmap_description_label = QLabel("Visualize customer engagement hotspots\nin real-time with our Heat-Map feature\nOptimizing your\nstore layout for maximum impact.")
        self.heatmap_description_label.setObjectName("heatmap_description_label")
        
        heatmap_layout.addWidget(heatmap_label)
        heatmap_layout.addWidget(self.heatmap_description_label)
        
        #heatmap_frame.setStyleSheet("QFrame { border: 2px solid black }")
        
        # Emotion Analysis Description
        emotion_frame = QFrame()
        emotion_frame.setFrameShape(QFrame.StyledPanel)
        emotion_frame.setFrameShadow(QFrame.Raised)
        emotion_frame.setFixedSize(400, 500)
        
        emotion_layout = QVBoxLayout(emotion_frame)
        
        emotion_pixmap = QPixmap(emotion_image_path)
        emotion_label = QLabel()
        emotion_label.setObjectName("emotion_label")
        emotion_label.setPixmap(emotion_pixmap)
        emotion_label.setScaledContents(True)
        
        emotion_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        emotion_label.setMinimumSize(300, 300)
        emotion_label.setMaximumSize(300, 300)
        emotion_label.setAlignment(Qt.AlignCenter)
        
        self.emotion_description_label = QLabel("Elevate customer experiences\nby detecting emotions allowing\npersonalized interactions and a\ndeeper understanding of your clientele.")
        self.emotion_description_label.setObjectName("emotion_description_label")
        
        emotion_layout.addWidget(emotion_label)
        emotion_layout.addWidget(self.emotion_description_label)
        
        overview_layout.addWidget(heatmap_frame)
        overview_layout.addWidget(emotion_frame)
        
        main_layout.addLayout(overview_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setObjectName("scroll_area")
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_widget)
        
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        
        with open('styles/main_page_styles.qss', 'r') as style_file:
            self.setStyleSheet(style_file.read())