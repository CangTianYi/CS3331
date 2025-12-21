# -*- coding: utf-8 -*-
# views/register_dialog.py
"""
Register Dialog: User registration form.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, 
    QLabel, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class RegisterDialog(QDialog):
    """Registration dialog with user details."""
    
    register_requested = pyqtSignal(str, str, str, str, str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register - Campus Xianyu")
        self.setFixedSize(450, 500)
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        # Title
        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Form
        form = QFormLayout()
        form.setSpacing(12)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMinimumHeight(38)
        form.addRow("Username *", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("At least 6 characters")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(38)
        form.addRow("Password *", self.password_input)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Re-enter password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setMinimumHeight(38)
        form.addRow("Confirm *", self.confirm_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@campus.edu")
        self.email_input.setMinimumHeight(38)
        form.addRow("Email", self.email_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone number")
        self.phone_input.setMinimumHeight(38)
        form.addRow("Phone", self.phone_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Dormitory address")
        self.address_input.setMinimumHeight(38)
        form.addRow("Address", self.address_input)

        layout.addLayout(form)

        # Note
        note = QLabel("* Registration requires admin approval")
        note.setStyleSheet("color: #E74C3C; font-size: 12px;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note)

        # Buttons
        self.register_btn = QPushButton("Submit Registration")
        self.register_btn.setObjectName("PrimaryButton")
        self.register_btn.setMinimumHeight(45)
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.register_btn)

        self.back_btn = QPushButton("Back to Login")
        self.back_btn.setMinimumHeight(40)
        layout.addWidget(self.back_btn)

        # Connections
        self.register_btn.clicked.connect(self.on_register_clicked)
        self.back_btn.clicked.connect(self.reject)

    def on_register_clicked(self):
        self.register_requested.emit(
            self.username_input.text().strip(),
            self.password_input.text(),
            self.confirm_input.text(),
            self.email_input.text().strip(),
            self.phone_input.text().strip(),
            self.address_input.text().strip()
        )

    def show_error(self, message: str):
        QMessageBox.warning(self, "Registration Failed", message)

    def show_success(self):
        QMessageBox.information(
            self, "Registration Successful", 
            "Your account has been submitted. Please wait for admin approval."
        )
        self.accept()
