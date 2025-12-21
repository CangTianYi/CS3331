# -*- coding: utf-8 -*-
# views/components/item_card.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor

class ItemCard(QFrame):
    clicked = pyqtSignal(str) # item_id

    def __init__(self, item_id: str, name: str, description: str, contact: str, parent=None):
        super().__init__(parent)
        self.item_id = item_id
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("ItemCard")
        self.setFixedWidth(220)
        self.setMinimumHeight(280)
        
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
        layout.setContentsMargins(15, 15, 15, 15)

        # Image setup (Placeholder for now)
        self.image_label = QLabel()
        self.image_label.setFixedSize(190, 150)
        self.image_label.setStyleSheet("background-color: #ECF0F1; border-radius: 5px;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("No Image")
        layout.addWidget(self.image_label)
        
        # Title
        self.lbl_name = QLabel(name)
        self.lbl_name.setStyleSheet("font-weight: bold; font-size: 16px; color: #2C3E50;")
        self.lbl_name.setWordWrap(True)
        layout.addWidget(self.lbl_name)

        # Description
        self.lbl_desc = QLabel(description)
        self.lbl_desc.setStyleSheet("color: #7F8C8D; font-size: 12px;")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setFixedHeight(40) # Limit height
        layout.addWidget(self.lbl_desc)

        # Contact
        self.lbl_contact = QLabel(contact)
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
