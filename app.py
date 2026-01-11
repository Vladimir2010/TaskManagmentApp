from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import sys
import os
from views.ui_utils import FluentStyle
from config import Config

class TaskManagerApp:
    def __init__(self, sys_argv):
        self.app = QApplication(sys_argv)
        self.app.setApplicationName(Config.APP_NAME)
        self.app.setApplicationVersion(Config.VERSION)
        
        # Set App Icon
        icon_path = os.path.join(Config.ASSETS_DIR, 'vladpos_logo.png')
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
        
        # Apply Global Fluent Style
        FluentStyle.apply_dark_theme(self.app)

    def exec(self):
        return self.app.exec()
