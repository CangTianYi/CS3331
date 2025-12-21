# -*- coding: utf-8 -*-
# views/main_window.py
"""
Main Window: User dashboard with category filtering and item display.
"""
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QScrollArea, QLabel, QFrame, QComboBox
)
from PyQt6.QtCore import pyqtSignal, Qt, QFile, QTextStream

from views.components.flow_layout import FlowLayout
from views.components.item_card import ItemCard

class MainWindow(QWidget):
    """Main user dashboard with category-based browsing."""
    
    # Signals
    add_item_requested = pyqtSignal()
    delete_item_requested = pyqtSignal(int)
    search_requested = pyqtSignal(int, str)
    category_changed = pyqtSignal(int)
    logout_requested = pyqtSignal()
    admin_panel_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campus Xianyu - Item Revival System")
        self.setGeometry(200, 200, 1000, 750)
        
        self._load_styles()
        
        self._selected_item_id: Optional[int] = None
        self._cards: Dict[int, ItemCard] = {}
        self._current_user = None
        self._item_types = []

        self.setup_ui()

    def _load_styles(self):
        file = QFile("assets/styles.qss")
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Top Bar
        top_bar = QHBoxLayout()
        
        title_label = QLabel("Campus Xianyu")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        top_bar.addWidget(title_label)
        
        top_bar.addStretch()

        self.user_label = QLabel("Not logged in")
        self.user_label.setStyleSheet("color: #7F8C8D; margin-right: 10px;")
        top_bar.addWidget(self.user_label)

        self.admin_btn = QPushButton("Admin Panel")
        self.admin_btn.setStyleSheet("background-color: #9B59B6; color: white; border: none;")
        self.admin_btn.setVisible(False)
        self.admin_btn.clicked.connect(self.admin_panel_requested.emit)
        top_bar.addWidget(self.admin_btn)

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setStyleSheet("color: #E74C3C;")
        self.logout_btn.clicked.connect(self.logout_requested.emit)
        top_bar.addWidget(self.logout_btn)
        
        main_layout.addLayout(top_bar)

        # Filter Bar
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(15)

        cat_label = QLabel("Category:")
        cat_label.setStyleSheet("font-weight: bold;")
        filter_bar.addWidget(cat_label)

        self.category_combo = QComboBox()
        self.category_combo.setMinimumWidth(150)
        self.category_combo.setMinimumHeight(35)
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)
        filter_bar.addWidget(self.category_combo)

        filter_bar.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or description...")
        self.search_input.setFixedWidth(250)
        self.search_input.setMinimumHeight(35)
        filter_bar.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("PrimaryButton")
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_button.setMinimumHeight(35)
        filter_bar.addWidget(self.search_button)
        
        self.clear_search_button = QPushButton("Clear")
        self.clear_search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_search_button.setMinimumHeight(35)
        filter_bar.addWidget(self.clear_search_button)
        
        main_layout.addLayout(filter_bar)

        # Content Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ScrollContents")
        self.flow_layout = FlowLayout(self.scroll_content, margin=10, h_spacing=20, v_spacing=20)
        
        scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(scroll_area)

        # Bottom Bar
        action_layout = QHBoxLayout()
        
        self.add_button = QPushButton("+ Post New Item")
        self.add_button.setObjectName("PrimaryButton")
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.setMinimumHeight(45)
        action_layout.addWidget(self.add_button)
        
        action_layout.addStretch()
        
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setEnabled(False)
        self.delete_button.setMinimumHeight(45)
        self.delete_button.setStyleSheet("color: #E74C3C; border-color: #E74C3C;")
        action_layout.addWidget(self.delete_button)
        
        main_layout.addLayout(action_layout)

        # Connections
        self.add_button.clicked.connect(self.add_item_requested.emit)
        self.search_button.clicked.connect(self.on_search_clicked)
        self.search_input.returnPressed.connect(self.on_search_clicked)
        self.clear_search_button.clicked.connect(self.on_clear_search_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)

    def set_current_user(self, user: dict):
        """Set the current logged-in user."""
        self._current_user = user
        if user:
            role_text = "(Admin)" if user['role'] == 'admin' else ""
            self.user_label.setText(f"Welcome, {user['username']} {role_text}")
            self.admin_btn.setVisible(user['role'] == 'admin')
        else:
            self.user_label.setText("Not logged in")
            self.admin_btn.setVisible(False)

    def set_item_types(self, types: list):
        """Update category dropdown."""
        self._item_types = types
        self.category_combo.blockSignals(True)
        self.category_combo.clear()
        
        if not types:
            self.category_combo.addItem("(No types)", 0)
        else:
            for t in types:
                self.category_combo.addItem(t['name'], t['id'])
        
        self.category_combo.blockSignals(False)
        
        if types:
            self.category_changed.emit(types[0]['id'])

    def get_selected_type_id(self) -> int:
        return self.category_combo.currentData() or 0

    def on_category_changed(self):
        type_id = self.category_combo.currentData()
        if type_id:
            self.category_changed.emit(type_id)

    def on_card_clicked(self, item_id: int):
        if self._selected_item_id and self._selected_item_id in self._cards:
            self._cards[self._selected_item_id].set_selected(False)
        
        self._selected_item_id = item_id
        if item_id in self._cards:
            self._cards[item_id].set_selected(True)
            
        self.delete_button.setEnabled(True)

    def on_search_clicked(self):
        type_id = self.get_selected_type_id()
        keyword = self.search_input.text().strip()
        self.search_requested.emit(type_id, keyword)
        
    def on_clear_search_clicked(self):
        self.search_input.clear()
        self.on_category_changed()

    def on_delete_clicked(self):
        if self._selected_item_id:
            self.delete_item_requested.emit(self._selected_item_id)

    def update_view(self, items: List[Dict]):
        """Refresh the grid of cards."""
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self._cards.clear()
        self._selected_item_id = None
        self.delete_button.setEnabled(False)

        for item in items:
            custom_text = ""
            custom_values = item.get('custom_values', {})
            if custom_values:
                custom_text = " | ".join([f"{k}: {v}" for k, v in custom_values.items()])
            
            description = item.get('description', '')
            if custom_text:
                description = f"{description}\n\n{custom_text}"
            
            card = ItemCard(
                item_id=str(item['id']),
                name=item['name'],
                description=description,
                contact=f"{item.get('contact_phone', '')} | {item.get('location', '')}"
            )
            # Disconnect existing clicked connection if any
            try:
                card.clicked.disconnect()
            except TypeError:
                pass  # No connections to disconnect
            card.item_id_int = item['id']
            card.clicked.connect(lambda id_str, iid=item['id']: self.on_card_clicked(iid))
            
            self.flow_layout.addWidget(card)
            self._cards[item['id']] = card

    def get_selected_item_name(self) -> Optional[str]:
        if self._selected_item_id and self._selected_item_id in self._cards:
            return self._cards[self._selected_item_id].lbl_name.text()
        return None
