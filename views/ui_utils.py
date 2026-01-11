from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtCore import Qt
import ctypes
from ctypes import c_int, byref

class FluentStyle:
    # Colors
    BACKGROUND_DARK = "#202020"
    BACKGROUND_LIGHT = "#F3F3F3"
    ACCENT = "#0078D4"
    TEXT_DARK = "#FFFFFF"
    TEXT_LIGHT = "#000000"
    SURFACE_DARK = "#2D2D2D"
    SURFACE_LIGHT = "#FFFFFF"

    @staticmethod
    def default_font():
        return QFont("Segoe UI Variable Display", 10)

    @staticmethod
    def title_font():
        return QFont("Segoe UI Variable Display", 14, QFont.Weight.Bold)

    @staticmethod
    def apply_dark_theme(app):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(FluentStyle.BACKGROUND_DARK))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(FluentStyle.TEXT_DARK))
        palette.setColor(QPalette.ColorRole.Base, QColor(FluentStyle.SURFACE_DARK))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(FluentStyle.BACKGROUND_DARK))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(FluentStyle.TEXT_DARK))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(FluentStyle.TEXT_LIGHT))
        palette.setColor(QPalette.ColorRole.Text, QColor(FluentStyle.TEXT_DARK))
        palette.setColor(QPalette.ColorRole.Button, QColor(FluentStyle.SURFACE_DARK))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(FluentStyle.TEXT_DARK))
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(FluentStyle.ACCENT))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(FluentStyle.ACCENT))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        app.setPalette(palette)
        
        app.setStyleSheet(f"""
            QWidget {{
                font-family: 'Segoe UI Variable Display', 'Segoe UI', sans-serif;
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {FluentStyle.SURFACE_DARK};
                border: 1px solid #3E3E3E;
                border-radius: 5px;
                padding: 6px 12px;
                color: {FluentStyle.TEXT_DARK};
            }}
            QPushButton:hover {{
                background-color: #3E3E3E;
            }}
            QPushButton:pressed {{
                background-color: #1F1F1F;
            }}
            QLineEdit {{
                background-color: {FluentStyle.SURFACE_DARK};
                border: 1px solid #3E3E3E;
                border-radius: 5px;
                padding: 6px;
                color: {FluentStyle.TEXT_DARK};
                selection-background-color: {FluentStyle.ACCENT};
            }}
            QLabel {{
                color: {FluentStyle.TEXT_DARK};
            }}
        """)

class WindowEffect:
    @staticmethod
    def apply_mica(hwnd, dark_mode=True):
        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_MICA_EFFECT = 1029
            
            # Enable Dark Mode for Title Bar
            value = c_int(1 if dark_mode else 0)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(value), 4)
            
            # Enable Mica (Windows 11 only)
            value = c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_MICA_EFFECT, byref(value), 4)
        except:
            pass # Fail silently on older Windows
