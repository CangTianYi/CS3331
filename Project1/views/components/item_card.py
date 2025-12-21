# -*- coding: utf-8 -*-
# views/components/item_card.py
import os
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor, QFontMetrics, QPixmap

class ItemCard(QFrame):
    clicked = pyqtSignal(str) # item_id

    def __init__(self, item_id: str, name: str, description: str, contact: str, 
                 image_path: str = None, parent=None):
        super().__init__(parent)
        self.item_id = item_id
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("ItemCard")
        self.setFixedWidth(250)  # Wider to fit Chinese text
        self.setMinimumHeight(300)
        
        # Style
        self.setStyleSheet("""
            #ItemCard {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
            #ItemCard:hover {
                border: 2px solid #3498DB;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Image setup
        self.image_label = QLabel()
        self.image_label.setFixedHeight(140)
        self.image_label.setStyleSheet("background-color: #ECF0F1; border-radius: 5px;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Load image if path provided
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled = pixmap.scaled(
                226, 140,  # card width - margins
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
        else:
            self.image_label.setText("No Image")
        layout.addWidget(self.image_label)
        
        # Title - Allow enough space
        self.lbl_name = QLabel(name)
        self.lbl_name.setStyleSheet("font-weight: bold; font-size: 14px; color: #2C3E50;")
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setMinimumHeight(20)
        layout.addWidget(self.lbl_name)

        # Description - truncate if too long
        desc_text = description[:80] + "..." if len(description) > 80 else description
        self.lbl_desc = QLabel(desc_text)
        self.lbl_desc.setStyleSheet("color: #7F8C8D; font-size: 12px;")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setMinimumHeight(36)
        self.lbl_desc.setMaximumHeight(50)
        layout.addWidget(self.lbl_desc)

        # Contact info - truncate if too long
        contact_text = contact[:40] + "..." if len(contact) > 40 else contact
        self.lbl_contact = QLabel(contact_text)
        self.lbl_contact.setStyleSheet("color: #95A5A6; font-size: 11px;")
        self.lbl_contact.setWordWrap(True)
        layout.addWidget(self.lbl_contact)
        
        layout.addStretch()

        self._selected = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.item_id)
        super().mousePressEvent(event)

    def set_selected(self, selected: bool):
        self._selected = selected
        if selected:
            self.setStyleSheet("""
                #ItemCard {
                    background-color: #EBF5FB;
                    border: 2px solid #3498DB;
                    border-radius: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                #ItemCard {
                    background-color: white;
                    border: 1px solid #E0E0E0;
                    border-radius: 10px;
                }
                #ItemCard:hover {
                    border: 2px solid #3498DB;
                }
            """)


