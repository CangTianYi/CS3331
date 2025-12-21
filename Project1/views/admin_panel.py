# -*- coding: utf-8 -*-
# views/admin_panel.py
"""
Admin Panel: Manage item types and approve users.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal

from views.type_editor_dialog import TypeEditorDialog

class AdminPanel(QWidget):
    """Admin panel with tabs for managing types and users."""
    
    # Signals
    type_created = pyqtSignal(str, list)
    type_updated = pyqtSignal(int, str, list)
    type_deleted = pyqtSignal(int)
    user_approved = pyqtSignal(int)
    user_rejected = pyqtSignal(int)
    back_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self._types = []
        self._pending_users = []

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QHBoxLayout()
        title = QLabel("Admin Panel")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        header.addWidget(title)
        header.addStretch()
        
        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(self.back_requested.emit)
        header.addWidget(back_btn)
        layout.addLayout(header)

        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Item Types
        self.types_tab = QWidget()
        self.setup_types_tab()
        self.tabs.addTab(self.types_tab, "Item Types")
        
        # Tab 2: Pending Users
        self.users_tab = QWidget()
        self.setup_users_tab()
        self.tabs.addTab(self.users_tab, "User Approval")
        
        layout.addWidget(self.tabs)

    def setup_types_tab(self):
        layout = QVBoxLayout(self.types_tab)
        layout.setContentsMargins(10, 15, 10, 10)

        add_btn = QPushButton("+ New Item Type")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setMinimumHeight(40)
        add_btn.clicked.connect(self.on_add_type)
        layout.addWidget(add_btn)

        self.types_table = QTableWidget()
        self.types_table.setColumnCount(4)
        self.types_table.setHorizontalHeaderLabels(["ID", "Type Name", "Custom Attributes", "Actions"])
        self.types_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.types_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.types_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.types_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.types_table.setColumnWidth(0, 50)
        self.types_table.setColumnWidth(3, 150)
        self.types_table.verticalHeader().setVisible(False)
        self.types_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.types_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.types_table)

    def setup_users_tab(self):
        layout = QVBoxLayout(self.users_tab)
        layout.setContentsMargins(10, 15, 10, 10)

        hint = QLabel("The following users are awaiting approval:")
        hint.setStyleSheet("color: #7F8C8D; margin-bottom: 10px;")
        layout.addWidget(hint)

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(["ID", "Username", "Email", "Phone", "Address", "Actions"])
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.users_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        self.users_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
        self.users_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.users_table.setColumnWidth(0, 50)
        self.users_table.setColumnWidth(5, 150)
        self.users_table.verticalHeader().setVisible(False)
        self.users_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.users_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.users_table)

    def update_types(self, types: list):
        """Refresh item types table."""
        self._types = types
        self.types_table.setRowCount(0)
        
        for t in types:
            row = self.types_table.rowCount()
            self.types_table.insertRow(row)
            
            self.types_table.setItem(row, 0, QTableWidgetItem(str(t['id'])))
            self.types_table.setItem(row, 1, QTableWidgetItem(t['name']))
            
            attrs = t.get('custom_attributes', [])
            attr_names = ', '.join([a['name'] for a in attrs]) if attrs else '(none)'
            self.types_table.setItem(row, 2, QTableWidgetItem(attr_names))
            
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 2, 5, 2)
            action_layout.setSpacing(5)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("padding: 4px 8px;")
            edit_btn.clicked.connect(lambda checked, type_data=t: self.on_edit_type(type_data))
            
            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet("padding: 4px 8px; color: #E74C3C;")
            del_btn.clicked.connect(lambda checked, type_id=t['id']: self.on_delete_type(type_id))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(del_btn)
            self.types_table.setCellWidget(row, 3, action_widget)

    def update_pending_users(self, users: list):
        """Refresh pending users table."""
        self._pending_users = users
        self.users_table.setRowCount(0)
        
        for u in users:
            row = self.users_table.rowCount()
            self.users_table.insertRow(row)
            
            self.users_table.setItem(row, 0, QTableWidgetItem(str(u['id'])))
            self.users_table.setItem(row, 1, QTableWidgetItem(u['username']))
            self.users_table.setItem(row, 2, QTableWidgetItem(u.get('email', '')))
            self.users_table.setItem(row, 3, QTableWidgetItem(u.get('phone', '')))
            self.users_table.setItem(row, 4, QTableWidgetItem(u.get('address', '')))
            
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 2, 5, 2)
            action_layout.setSpacing(5)
            
            approve_btn = QPushButton("Approve")
            approve_btn.setStyleSheet("padding: 4px 8px; background-color: #27AE60; color: white; border: none;")
            approve_btn.clicked.connect(lambda checked, user_id=u['id']: self.on_approve_user(user_id))
            
            reject_btn = QPushButton("Reject")
            reject_btn.setStyleSheet("padding: 4px 8px; color: #E74C3C;")
            reject_btn.clicked.connect(lambda checked, user_id=u['id']: self.on_reject_user(user_id))
            
            action_layout.addWidget(approve_btn)
            action_layout.addWidget(reject_btn)
            self.users_table.setCellWidget(row, 5, action_widget)

    def on_add_type(self):
        dialog = TypeEditorDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.type_created.emit(data['name'], data['custom_attributes'])

    def on_edit_type(self, type_data: dict):
        dialog = TypeEditorDialog(self, type_data)
        if dialog.exec():
            data = dialog.get_data()
            self.type_updated.emit(data['id'], data['name'], data['custom_attributes'])

    def on_delete_type(self, type_id: int):
        reply = QMessageBox.warning(
            self, "Confirm Delete",
            "Deleting this type will also delete all items of this type. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.type_deleted.emit(type_id)

    def on_approve_user(self, user_id: int):
        self.user_approved.emit(user_id)

    def on_reject_user(self, user_id: int):
        reply = QMessageBox.warning(
            self, "Confirm Reject",
            "Rejecting will delete this registration. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.user_rejected.emit(user_id)
