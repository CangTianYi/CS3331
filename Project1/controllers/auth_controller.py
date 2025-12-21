# -*- coding: utf-8 -*-
# controllers/auth_controller.py
"""
Authentication Controller: Login, Register, Session Management.
"""
from PyQt6.QtCore import QObject, pyqtSignal
from model.user_manager import UserManager

class AuthController(QObject):
    """Handles authentication flows."""
    
    # Signals
    login_success = pyqtSignal(dict)  # Emits user data
    login_failed = pyqtSignal(str)    # Emits error message
    register_success = pyqtSignal()
    register_failed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()
        self.current_user = None

    def login(self, username: str, password: str):
        """Attempt to login."""
        if not username or not password:
            self.login_failed.emit("Please enter username and password")
            return
        
        user = self.user_manager.login(username, password)
        
        if user:
            if user['role'] == 'pending':
                self.login_failed.emit("Your account is pending admin approval")
                return
            self.current_user = user
            self.login_success.emit(user)
        else:
            self.login_failed.emit("Invalid username or password")

    def register(self, username: str, password: str, confirm_password: str,
                 email: str, phone: str, address: str):
        """Attempt to register a new user."""
        # Validation
        if not username or not password:
            self.register_failed.emit("Username and password are required")
            return
        
        if password != confirm_password:
            self.register_failed.emit("Passwords do not match")
            return
        
        if len(password) < 6:
            self.register_failed.emit("Password must be at least 6 characters")
            return
        
        # Attempt registration
        result = self.user_manager.register(username, password, email, phone, address)
        
        if result:
            self.register_success.emit()
        else:
            self.register_failed.emit("Username already exists")

    def logout(self):
        """Clear current session."""
        self.current_user = None

    def is_admin(self) -> bool:
        """Check if current user is admin."""
        return self.current_user and self.current_user.get('role') == 'admin'

    def get_current_user(self) -> dict:
        """Get current logged-in user."""
        return self.current_user
