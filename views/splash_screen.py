from PyQt6.QtWidgets import QSplashScreen, QProgressBar
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt
import time
import os
from config import Config

class SplashScreen(QSplashScreen):
    def __init__(self, app_name, version):
        # Create a dynamic pixmap since we don't have an image file (or just text based on user request)
        pixmap = QPixmap(600, 300)
        pixmap.fill(QColor("#202020"))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Segoe UI Variable Display", 32, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, app_name)
        
        painter.setFont(QFont("Segoe UI", 12))
        painter.drawText(580, 290, version) # Bottom right
        painter.end()
        
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 280, 600, 20)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #202020;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #0078D4;
            }
        """)
        self.progress.setRange(0, 100)

    def show_progress(self, percent):
        self.progress.setValue(percent)
        self.repaint()
        # Simulate loading
        time.sleep(0.02)
