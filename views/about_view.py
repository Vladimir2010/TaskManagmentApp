from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from views.ui_utils import FluentStyle, WindowEffect
from services.language_service import lang_service
from config import Config
import os

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(lang_service.get("about_title"))
        self.setFixedSize(400, 300)
        self.setStyleSheet(f"background-color: {FluentStyle.BACKGROUND_DARK}; color: {FluentStyle.TEXT_DARK};")
        
        # Apply Mica if available
        self.window_effect = WindowEffect()
        self.window_effect.apply_mica(int(self.winId()), dark_mode=True)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(Config.ASSETS_DIR, "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # App Title
        title_label = QLabel(lang_service.get("app_title"))
        title_font = QFont("Segoe UI Variable Display", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Version
        version_label = QLabel(lang_service.get("app_version"))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"color: {FluentStyle.TEXT_SECONDARY};")
        layout.addWidget(version_label)
        
        # Description
        desc_label = QLabel(lang_service.get("app_description"))
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)
        
        # Developer Info
        dev_label = QLabel(lang_service.get("developer_info"))
        dev_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev_label.setStyleSheet(f"color: {FluentStyle.TEXT_SECONDARY}; font-style: italic;")
        layout.addWidget(dev_label)
        
        # Close Button
        close_btn = QPushButton("Close") # Simple "Close" usually sufficient or translate if needed
        # We can add a key for "close" if we want strictly everything translated
        close_btn.setText(lang_service.get("close", default="Close"))
        close_btn.setFixedSize(100, 35)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {FluentStyle.SURFACE_DARK};
                border: 1px solid {FluentStyle.BORDER_DARK};
                border-radius: 5px;
                color: {FluentStyle.TEXT_DARK};
            }}
            QPushButton:hover {{
                background-color: {FluentStyle.HOVER_DARK};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
