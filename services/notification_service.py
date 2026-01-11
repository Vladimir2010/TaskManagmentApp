from PyQt6.QtWidgets import QSystemTrayIcon
from PyQt6.QtGui import QIcon
from config import Config

class NotificationService:
    _tray_icon = None

    @staticmethod
    def setup_tray(app, icon_path):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        NotificationService._tray_icon = QSystemTrayIcon(QIcon(icon_path), app)
        NotificationService._tray_icon.show()

    @staticmethod
    def send_notification(title, message):
        if NotificationService._tray_icon:
            NotificationService._tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )
