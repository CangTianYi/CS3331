# -*- coding: utf-8 -*-
# controllers/admin_controller.py
"""
Admin Controller: Item Type Management, User Approval.
"""
from PyQt6.QtCore import QObject, pyqtSignal
from model.item_type_manager import ItemTypeManager
from model.user_manager import UserManager

class AdminController(QObject):
    """Handles admin-only operations."""
    
    # Signals
    types_updated = pyqtSignal()
    users_updated = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.type_manager = ItemTypeManager()
        self.user_manager = UserManager()

    # --- Item Type Management ---

    def get_all_types(self) -> list:
        """Get all item types."""
        return self.type_manager.get_all_types()

    def create_type(self, name: str, custom_attributes: list):
        """Create a new item type."""
        if not name:
            self.error_occurred.emit("Type name cannot be empty")
            return
        
        result = self.type_manager.create_type(name, custom_attributes)
        if result:
            self.types_updated.emit()
        else:
            self.error_occurred.emit("Type name already exists")

    def update_type(self, type_id: int, name: str, custom_attributes: list):
        """Update an existing item type."""
        if not name:
            self.error_occurred.emit("Type name cannot be empty")
            return
        
        self.type_manager.update_type(type_id, name, custom_attributes)
        self.types_updated.emit()

    def delete_type(self, type_id: int):
        """Delete an item type."""
        self.type_manager.delete_type(type_id)
        self.types_updated.emit()

    # --- User Management ---

    def get_pending_users(self) -> list:
        """Get all pending users."""
        return self.user_manager.get_pending_users()

    def approve_user(self, user_id: int):
        """Approve a pending user."""
        self.user_manager.approve_user(user_id)
        self.users_updated.emit()

    def reject_user(self, user_id: int):
        """Reject a pending user."""
        self.user_manager.reject_user(user_id)
        self.users_updated.emit()
