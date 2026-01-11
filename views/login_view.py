from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from views.ui_utils import FluentStyle, WindowEffect
from controllers.auth_controller import AuthController
from config import Config
import os

class LoginView(QMainWindow):
    login_success = pyqtSignal(object) # Emits user object

    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.setWindowTitle("Login - Task Manager Pro")
        self.resize(400, 500)
        
        # Apply Mica
        WindowEffect.apply_mica(int(self.winId()))
        
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Logo / Title
        title_label = QLabel("Task Manager Pro")
        title_label.setFont(QFont("Segoe UI Variable Display", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Form Container
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 10px; padding: 20px;")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        form_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.password_input)
        
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumHeight(35)
        self.login_btn.setStyleSheet("background-color: #0078D4; font-weight: bold;")
        self.login_btn.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton("Create Account")
        self.register_btn.setMinimumHeight(35)
        self.register_btn.clicked.connect(self.handle_register)
        form_layout.addWidget(self.register_btn)

        layout.addWidget(form_frame)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
            
        success, message = self.auth_controller.login(username, password)
        if success:
            self.login_success.emit(self.auth_controller.current_user)
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", message)

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields to register")
            return
            
        success, message = self.auth_controller.register(username, password, "")
        if success:
            QMessageBox.information(self, "Success", "Account created! You can now login.")
        else:
            QMessageBox.critical(self, "Error", message)
