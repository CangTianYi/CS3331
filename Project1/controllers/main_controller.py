# -*- coding: utf-8 -*-
# controllers/main_controller.py
"""
Main Controller: Orchestrates the application flow.
"""
from PyQt6.QtWidgets import QMessageBox, QStackedWidget
from PyQt6.QtCore import QObject

from model.item_manager import ItemManager
from model.item_type_manager import ItemTypeManager
from model.user_manager import UserManager

from controllers.auth_controller import AuthController
from controllers.admin_controller import AdminController

from views.main_window import MainWindow
from views.login_dialog import LoginDialog
from views.register_dialog import RegisterDialog
from views.admin_panel import AdminPanel
from views.add_item_dialog import AddItemDialog

class MainController(QObject):
    """Main application controller."""
    
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        
        self.stack = stacked_widget
        
        # Models
        self.item_manager = ItemManager()
        self.type_manager = ItemTypeManager()
        self.user_manager = UserManager()
        
        # Controllers
        self.auth_controller = AuthController()
        self.admin_controller = AdminController()
        
        # Views
        self.login_dialog = LoginDialog()
        self.register_dialog = RegisterDialog()
        self.main_window = MainWindow()
        self.admin_panel = AdminPanel()
        
        # Add views to stack
        self.stack.addWidget(self.login_dialog)
        self.stack.addWidget(self.register_dialog)
        self.stack.addWidget(self.main_window)
        self.stack.addWidget(self.admin_panel)
        
        # Connect signals
        self._connect_auth_signals()
        self._connect_main_signals()
        self._connect_admin_signals()

    def _connect_auth_signals(self):
        self.login_dialog.login_requested.connect(self.auth_controller.login)
        self.login_dialog.register_requested.connect(self.show_register)
        self.auth_controller.login_success.connect(self.on_login_success)
        self.auth_controller.login_failed.connect(self.login_dialog.show_error)
        
        self.register_dialog.register_requested.connect(self.auth_controller.register)
        self.register_dialog.back_to_login.connect(self.show_login)
        self.auth_controller.register_success.connect(self.register_dialog.show_success)
        self.auth_controller.register_failed.connect(self.register_dialog.show_error)

    def _connect_main_signals(self):
        self.main_window.logout_requested.connect(self.on_logout)
        self.main_window.admin_panel_requested.connect(self.show_admin_panel)
        self.main_window.category_changed.connect(self.load_items_by_type)
        self.main_window.search_requested.connect(self.handle_search)
        self.main_window.add_item_requested.connect(self.show_add_item_dialog)
        self.main_window.delete_item_requested.connect(self.handle_delete_item)

    def _connect_admin_signals(self):
        self.admin_panel.back_requested.connect(self.show_main_window)
        self.admin_panel.type_created.connect(self.admin_controller.create_type)
        self.admin_panel.type_updated.connect(self.admin_controller.update_type)
        self.admin_panel.type_deleted.connect(self.admin_controller.delete_type)
        self.admin_panel.user_approved.connect(self.admin_controller.approve_user)
        self.admin_panel.user_rejected.connect(self.admin_controller.reject_user)
        
        self.admin_controller.types_updated.connect(self.refresh_admin_types)
        self.admin_controller.users_updated.connect(self.refresh_admin_users)
        self.admin_controller.error_occurred.connect(
            lambda msg: QMessageBox.warning(self.admin_panel, "Error", msg)
        )

    def run(self):
        """Start the application."""
        self.stack.setCurrentWidget(self.login_dialog)
        self.stack.show()

    def on_login_success(self, user: dict):
        self.login_dialog.clear_inputs()
        self.main_window.set_current_user(user)
        
        types = self.type_manager.get_all_types()
        self.main_window.set_item_types(types)
        
        self.show_main_window()

    def on_logout(self):
        self.auth_controller.logout()
        self.main_window.set_current_user(None)
        self.stack.setCurrentWidget(self.login_dialog)

    def show_register(self):
        self.stack.setCurrentWidget(self.register_dialog)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_dialog)

    def show_main_window(self):
        types = self.type_manager.get_all_types()
        self.main_window.set_item_types(types)
        self.stack.setCurrentWidget(self.main_window)

    def load_items_by_type(self, type_id: int):
        items = self.item_manager.get_items_by_type(type_id)
        self.main_window.update_view(items)

    def handle_search(self, type_id: int, keyword: str):
        if keyword:
            items = self.item_manager.search_items(type_id, keyword)
        else:
            items = self.item_manager.get_items_by_type(type_id)
        self.main_window.update_view(items)

    def show_add_item_dialog(self):
        types = self.type_manager.get_all_types()
        if not types:
            QMessageBox.warning(
                self.main_window, "Notice",
                "No item types available. Please contact admin."
            )
            return
        
        dialog = AddItemDialog(self.main_window, types)
        if dialog.exec():
            data = dialog.get_data()
            user = self.auth_controller.get_current_user()
            
            self.item_manager.add_item(
                type_id=data['type_id'],
                owner_id=user['id'],
                name=data['name'],
                description=data['description'],
                location=data['location'],
                contact_phone=data['contact_phone'],
                contact_email=data['contact_email'],
                custom_values=data['custom_values']
            )
            
            current_type_id = self.main_window.get_selected_type_id()
            self.load_items_by_type(current_type_id)

    def handle_delete_item(self, item_id: int):
        item_name = self.main_window.get_selected_item_name() or "this item"
        user = self.auth_controller.get_current_user()
        
        reply = QMessageBox.warning(
            self.main_window,
            "Confirm Delete",
            f"Are you sure you want to delete '{item_name}'?\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.auth_controller.is_admin():
                self.item_manager.delete_item(item_id)
            else:
                self.item_manager.delete_item(item_id, user['id'])
            
            current_type_id = self.main_window.get_selected_type_id()
            self.load_items_by_type(current_type_id)

    def show_admin_panel(self):
        self.refresh_admin_types()
        self.refresh_admin_users()
        self.stack.setCurrentWidget(self.admin_panel)

    def refresh_admin_types(self):
        types = self.admin_controller.get_all_types()
        self.admin_panel.update_types(types)

    def refresh_admin_users(self):
        users = self.admin_controller.get_pending_users()
        self.admin_panel.update_pending_users(users)