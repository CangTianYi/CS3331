# -*- coding: utf-8 -*-
# views/type_editor_dialog.py
"""
Item Type Editor Dialog: Create or edit item types with custom attributes.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView,
    QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt

class TypeEditorDialog(QDialog):
    """Dialog for creating/editing item types with dynamic attributes."""
    
    def __init__(self, parent=None, item_type: dict = None):
        super().__init__(parent)
        self.item_type = item_type
        self.setWindowTitle("Edit Type" if item_type else "Create Type")
        self.setFixedSize(500, 450)
        self.setModal(True)
        self.setup_ui()
        
        if item_type:
            self.load_type_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Type Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Type Name:")
        name_label.setFixedWidth(80)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Books, Food, Tools")
        self.name_input.setMinimumHeight(35)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Custom Attributes Section
        attr_header = QLabel("Custom Attributes")
        attr_header.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        layout.addWidget(attr_header)

        attr_hint = QLabel("Add type-specific attributes (e.g. author for books, expiry for food)")
        attr_hint.setStyleSheet("color: #7F8C8D; font-size: 12px;")
        layout.addWidget(attr_hint)

        # Attributes Table
        self.attr_table = QTableWidget()
        self.attr_table.setColumnCount(3)
        self.attr_table.setHorizontalHeaderLabels(["Attribute Name", "Type", "Action"])
        self.attr_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.attr_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.attr_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.attr_table.setColumnWidth(1, 100)
        self.attr_table.setColumnWidth(2, 60)
        self.attr_table.verticalHeader().setVisible(False)
        self.attr_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        layout.addWidget(self.attr_table)

        # Add Attribute Button
        add_attr_btn = QPushButton("+ Add Attribute")
        add_attr_btn.clicked.connect(self.add_attribute_row)
        layout.addWidget(add_attr_btn)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setObjectName("PrimaryButton")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)

    def add_attribute_row(self, name: str = "", attr_type: str = "text"):
        """Add a new attribute row to the table."""
        row = self.attr_table.rowCount()
        self.attr_table.insertRow(row)

        name_input = QLineEdit(name)
        name_input.setPlaceholderText("Attribute name")
        self.attr_table.setCellWidget(row, 0, name_input)

        type_combo = QComboBox()
        type_combo.addItems(["text", "number", "date"])
        type_combo.setCurrentText(attr_type)
        self.attr_table.setCellWidget(row, 1, type_combo)

        del_btn = QPushButton("Delete")
        del_btn.setStyleSheet("color: #E74C3C;")
        del_btn.clicked.connect(lambda: self.remove_attribute_row(row))
        self.attr_table.setCellWidget(row, 2, del_btn)

    def remove_attribute_row(self, row: int):
        """Remove an attribute row."""
        self.attr_table.removeRow(row)
        for i in range(self.attr_table.rowCount()):
            del_btn = self.attr_table.cellWidget(i, 2)
            if del_btn:
                del_btn.clicked.disconnect()
                del_btn.clicked.connect(lambda checked, r=i: self.remove_attribute_row(r))

    def load_type_data(self):
        """Load existing type data into the form."""
        self.name_input.setText(self.item_type['name'])
        for attr in self.item_type.get('custom_attributes', []):
            self.add_attribute_row(attr['name'], attr.get('type', 'text'))

    def get_data(self) -> dict:
        """Get form data as dict."""
        attributes = []
        for row in range(self.attr_table.rowCount()):
            name_widget = self.attr_table.cellWidget(row, 0)
            type_widget = self.attr_table.cellWidget(row, 1)
            if name_widget and type_widget:
                attr_name = name_widget.text().strip()
                if attr_name:
                    attributes.append({
                        'name': attr_name,
                        'type': type_widget.currentText()
                    })
        
        return {
            'id': self.item_type['id'] if self.item_type else None,
            'name': self.name_input.text().strip(),
            'custom_attributes': attributes
        }

    def on_save(self):
        """Validate and accept."""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Error", "Please enter type name")
            return
        self.accept()
