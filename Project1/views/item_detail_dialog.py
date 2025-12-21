# -*- coding: utf-8 -*-
# views/item_detail_dialog.py
"""
Item Detail Dialog: Shows full item information when card is clicked.
"""
import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QWidget, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class ItemDetailDialog(QDialog):
    """Dialog showing detailed item information."""
    
    def __init__(self, item_data: dict, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.setWindowTitle(f"Item Details - {item_data.get('name', 'Unknown')}")
        self.setMinimumSize(550, 500)
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Header
        header = QLabel(self.item_data.get('name', 'Unknown Item'))
        header.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #2C3E50;")
        header.setWordWrap(True)
        layout.addWidget(header)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #E0E0E0;")
        layout.addWidget(separator)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)

        # Image section
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setMinimumHeight(200)
        image_label.setStyleSheet("""
            background-color: #ECF0F1; 
            border-radius: 8px;
            font-size: 14px;
            color: #95A5A6;
        """)
        
        # Load image if path provided
        image_path = self.item_data.get('image_path')
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled = pixmap.scaled(
                450, 250,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(scaled)
        else:
            image_label.setText("No Image")
        content_layout.addWidget(image_label)

        # Info sections
        self._add_info_row(content_layout, "Category", self.item_data.get('type_name', 'N/A'))
        self._add_info_row(content_layout, "Description", self.item_data.get('description', 'No description'))
        self._add_info_row(content_layout, "Location", self.item_data.get('location', 'N/A'))
        self._add_info_row(content_layout, "Posted by", self.item_data.get('owner_name', 'Unknown'))
        self._add_info_row(content_layout, "Phone", self.item_data.get('contact_phone', 'N/A'))
        self._add_info_row(content_layout, "Email", self.item_data.get('contact_email', 'N/A'))
        
        # Custom attributes
        custom_values = self.item_data.get('custom_values', {})
        if custom_values:
            content_layout.addWidget(self._create_section_header("Additional Details"))
            for key, value in custom_values.items():
                self._add_info_row(content_layout, key, str(value))

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        # Close button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setMinimumSize(100, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
        """)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)

    def _add_info_row(self, layout: QVBoxLayout, label: str, value: str):
        """Add an info row with label and value."""
        row = QHBoxLayout()
        
        lbl = QLabel(f"{label}:")
        lbl.setStyleSheet("font-weight: bold; color: #34495E; font-size: 13px;")
        lbl.setFixedWidth(100)
        row.addWidget(lbl)
        
        val = QLabel(value or "N/A")
        val.setStyleSheet("color: #2C3E50; font-size: 13px;")
        val.setWordWrap(True)
        row.addWidget(val, stretch=1)
        
        layout.addLayout(row)

    def _create_section_header(self, text: str) -> QLabel:
        """Create a section header label."""
        lbl = QLabel(text)
        lbl.setStyleSheet("""
            font-weight: bold; 
            color: #3498DB; 
            font-size: 14px;
            margin-top: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid #E0E0E0;
        """)
        return lbl
