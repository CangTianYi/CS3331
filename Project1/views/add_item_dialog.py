# -*- coding: utf-8 -*-
# views/add_item_dialog.py
"""
Add Item Dialog: Two-step form with type selection and dynamic fields.
"""
import os
import shutil
import uuid
from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QTextEdit, QPushButton, QFormLayout, 
    QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QMessageBox,
    QStackedWidget, QWidget, QDateEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap

class AddItemDialog(QDialog):
    """Dialog for adding a new item."""
    
    def __init__(self, parent=None, item_types: list = None):
        super().__init__(parent)
        self.setWindowTitle("Post New Item")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        self._item_types = item_types or []
        self._selected_type = None
        self._custom_inputs = {}
        self._selected_image_path = None  # Store selected image path
        
        # Create uploads directory if it doesn't exist
        self._uploads_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            "uploads"
        )
        os.makedirs(self._uploads_dir, exist_ok=True)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("Post New Item")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.stack = QStackedWidget()
        
        self.step1 = QWidget()
        self.setup_step1()
        self.stack.addWidget(self.step1)
        
        self.step2 = QWidget()
        self.step2_layout = QVBoxLayout(self.step2)
        self.step2_layout.setContentsMargins(0, 0, 0, 0)
        self.stack.addWidget(self.step2)
        
        layout.addWidget(self.stack)

    def setup_step1(self):
        layout = QVBoxLayout(self.step1)
        layout.setSpacing(20)

        hint = QLabel("Select item type:")
        hint.setStyleSheet("font-size: 14px;")
        layout.addWidget(hint)

        self.type_combo = QComboBox()
        self.type_combo.setMinimumHeight(40)
        for t in self._item_types:
            self.type_combo.addItem(t['name'], t)
        layout.addWidget(self.type_combo)

        layout.addStretch()

        nav = QHBoxLayout()
        nav.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        nav.addWidget(cancel_btn)
        
        next_btn = QPushButton("Next")
        next_btn.setObjectName("PrimaryButton")
        next_btn.setMinimumHeight(40)
        next_btn.clicked.connect(self.go_to_step2)
        nav.addWidget(next_btn)
        
        layout.addLayout(nav)

    def go_to_step2(self):
        self._selected_type = self.type_combo.currentData()
        if not self._selected_type:
            QMessageBox.warning(self, "Error", "Please select an item type")
            return
        
        self.build_step2_form()
        self.stack.setCurrentIndex(1)

    def build_step2_form(self):
        while self.step2_layout.count():
            child = self.step2_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self._custom_inputs.clear()
        self._selected_image_path = None
        
        form = QFormLayout()
        form.setSpacing(12)

        type_label = QLabel(f"Type: {self._selected_type['name']}")
        type_label.setStyleSheet("font-weight: bold; color: #3498DB; margin-bottom: 10px;")
        self.step2_layout.addWidget(type_label)

        # Image Upload Section
        image_section = QVBoxLayout()
        image_label = QLabel("Item Image")
        image_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        image_section.addWidget(image_label)
        
        image_row = QHBoxLayout()
        
        self.image_preview = QLabel("No image selected")
        self.image_preview.setFixedSize(120, 90)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setStyleSheet("""
            background-color: #ECF0F1; 
            border: 1px dashed #BDC3C7;
            border-radius: 5px;
            color: #7F8C8D;
            font-size: 11px;
        """)
        image_row.addWidget(self.image_preview)
        
        image_btn_layout = QVBoxLayout()
        self.select_image_btn = QPushButton("Select Image")
        self.select_image_btn.setMinimumHeight(35)
        self.select_image_btn.clicked.connect(self.select_image)
        image_btn_layout.addWidget(self.select_image_btn)
        
        self.clear_image_btn = QPushButton("Clear")
        self.clear_image_btn.setMinimumHeight(30)
        self.clear_image_btn.clicked.connect(self.clear_image)
        self.clear_image_btn.setEnabled(False)
        image_btn_layout.addWidget(self.clear_image_btn)
        image_btn_layout.addStretch()
        
        image_row.addLayout(image_btn_layout)
        image_row.addStretch()
        
        image_section.addLayout(image_row)
        self.step2_layout.addLayout(image_section)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item name")
        self.name_input.setMinimumHeight(35)
        form.addRow("Name *", self.name_input)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Description")
        self.desc_input.setMaximumHeight(80)
        form.addRow("Description", self.desc_input)

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("e.g. Dorm Building 5")
        self.location_input.setMinimumHeight(35)
        form.addRow("Location *", self.location_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone number")
        self.phone_input.setMinimumHeight(35)
        form.addRow("Phone *", self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email address")
        self.email_input.setMinimumHeight(35)
        form.addRow("Email", self.email_input)

        custom_attrs = self._selected_type.get('custom_attributes', [])
        if custom_attrs:
            separator = QLabel("-- Type-specific attributes --")
            separator.setStyleSheet("color: #7F8C8D; margin-top: 10px;")
            separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
            form.addRow(separator)

        for attr in custom_attrs:
            attr_name = attr['name']
            attr_type = attr.get('type', 'text')
            
            if attr_type == 'number':
                widget = QLineEdit()
                widget.setPlaceholderText("Number")
                widget.setMinimumHeight(35)
            elif attr_type == 'date':
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                widget.setDate(QDate.currentDate())
                widget.setMinimumHeight(35)
            else:
                widget = QLineEdit()
                widget.setPlaceholderText(attr_name)
                widget.setMinimumHeight(35)
            
            self._custom_inputs[attr_name] = widget
            form.addRow(f"{attr_name}", widget)

        self.step2_layout.addLayout(form)
        self.step2_layout.addStretch()

        nav = QHBoxLayout()
        
        back_btn = QPushButton("Back")
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        nav.addWidget(back_btn)
        
        nav.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        nav.addWidget(cancel_btn)
        
        save_btn = QPushButton("Post")
        save_btn.setObjectName("PrimaryButton")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.on_save)
        nav.addWidget(save_btn)
        
        self.step2_layout.addLayout(nav)

    def select_image(self):
        """Open file dialog to select an image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Image", 
            "", 
            "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            self._selected_image_path = file_path
            # Show preview
            pixmap = QPixmap(file_path)
            scaled = pixmap.scaled(
                self.image_preview.size(), 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_preview.setPixmap(scaled)
            self.clear_image_btn.setEnabled(True)

    def clear_image(self):
        """Clear selected image."""
        self._selected_image_path = None
        self.image_preview.setText("No image selected")
        self.image_preview.setPixmap(QPixmap())
        self.clear_image_btn.setEnabled(False)

    def copy_image_to_uploads(self) -> str:
        """Copy selected image to uploads folder and return new path."""
        if not self._selected_image_path:
            return None
        
        # Generate unique filename
        ext = os.path.splitext(self._selected_image_path)[1]
        new_filename = f"{uuid.uuid4().hex}{ext}"
        new_path = os.path.join(self._uploads_dir, new_filename)
        
        try:
            shutil.copy2(self._selected_image_path, new_path)
            return new_path
        except Exception as e:
            print(f"Error copying image: {e}")
            return None

    def get_data(self) -> dict:
        # Safety check: ensure step 2 form was built
        if not hasattr(self, 'name_input') or self._selected_type is None:
            return {}
        
        custom_values = {}
        for attr_name, widget in self._custom_inputs.items():
            if isinstance(widget, QDateEdit):
                custom_values[attr_name] = widget.date().toString("yyyy-MM-dd")
            else:
                custom_values[attr_name] = widget.text().strip()
        
        # Copy image to uploads if selected
        image_path = self.copy_image_to_uploads()
        
        return {
            "type_id": self._selected_type['id'],
            "name": self.name_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "location": self.location_input.text().strip(),
            "contact_phone": self.phone_input.text().strip(),
            "contact_email": self.email_input.text().strip(),
            "image_path": image_path,
            "custom_values": custom_values
        }

    def validate_input(self) -> bool:
        data = self.get_data()
        if not data.get("name"):
            QMessageBox.warning(self, "Notice", "Please enter item name")
            return False
        if not data.get("location"):
            QMessageBox.warning(self, "Notice", "Please enter location")
            return False
        if not data.get("contact_phone"):
            QMessageBox.warning(self, "Notice", "Please enter phone number")
            return False
        return True

    def on_save(self):
        if self.validate_input():
            self.accept()
