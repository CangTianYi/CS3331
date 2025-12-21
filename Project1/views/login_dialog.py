# -*- coding: utf-8 -*-
# views/login_dialog.py
"""
Login Dialog: Username/Password authentication.
"""
import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QLabel, QMessageBox, QFrame, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

class LoginDialog(QDialog):
    """Login dialog with username and password fields."""
    
    login_requested = pyqtSignal(str, str)  # username, password
    register_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Campus Xianyu")
        # Removed fixed size to support responsiveness
        self.setMinimumSize(900, 600)
        # Note: Do NOT set modal when used in QStackedWidget
        self.setup_ui()

    def setup_ui(self):
        # Main Layout: Horizontal (Left: Form, Right: Image)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Left Side: Login Form ---
        form_container = QWidget()
        form_container.setStyleSheet("background-color: white;")
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(50, 50, 50, 50)
        form_layout.setSpacing(20)

        # Title
        title = QLabel("Campus Xianyu")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")
        form_layout.addWidget(title)

        subtitle = QLabel("Campus Second-hand Item Revival")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        subtitle.setStyleSheet("color: #7F8C8D; margin-bottom: 30px; font-size: 16px;")
        form_layout.addWidget(subtitle)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(50)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498DB;
            }
        """)
        form_layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(50)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498DB;
            }
        """)
        form_layout.addWidget(self.password_input)

        # Login Button
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumHeight(55)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #1A252F;
            }
        """)
        form_layout.addWidget(self.login_btn)

        # Register Link
        register_layout = QHBoxLayout()
        register_label = QLabel("Don't have an account?")
        register_label.setStyleSheet("color: #7F8C8D; font-size: 14px;")
        register_layout.addWidget(register_label)
        
        self.register_btn = QPushButton("create an account")
        self.register_btn.setFlat(True)
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_btn.setStyleSheet("""
            QPushButton {
                color: #3498DB;
                font-weight: bold;
                border: none;
                font-size: 14px;
                text-align: left;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        register_layout.addWidget(self.register_btn)
        register_layout.addStretch()
        form_layout.addLayout(register_layout)
        
        form_layout.addStretch() # Push everything up

        # Add left container to main layout
        main_layout.addWidget(form_container, stretch=4)

        # --- Right Side: Image ---
        image_label = QLabel()
        image_label.setStyleSheet("background-color: #f0f2f5;") 
        
        # Load Image
        # Assuming assets folder is at the project root level, relative to this file: ../assets/login_bg.png
        # But safer to find it relative to the project root or this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        image_path = os.path.join(project_root, "assets", "login_bg.png")
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)  # Scale image to fit label
            image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        else:
            image_label.setText("Image not found: " + image_path)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add right image to main layout
        main_layout.addWidget(image_label, stretch=6)

        # Connections
        self.connect_signals()

    def connect_signals(self):
        self.login_btn.clicked.connect(self.on_login_clicked)
        self.password_input.returnPressed.connect(self.on_login_clicked)
        self.register_btn.clicked.connect(self.register_requested.emit)

    def on_login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        self.login_requested.emit(username, password)

    def show_error(self, message: str):
        QMessageBox.warning(self, "Login Failed", message)

    def clear_inputs(self):
        self.username_input.clear()
        self.password_input.clear()
