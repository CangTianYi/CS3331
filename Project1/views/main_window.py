# views/main_window.py
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QScrollArea, QLabel, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt, QFile, QTextStream

from views.components.flow_layout import FlowLayout
from views.components.item_card import ItemCard

class MainWindow(QWidget):
    """
    PRD 3.1: 主窗口 (View)
    Updated: Uses Card Grid Layout instead of Table.
    """
    
    # --- Signals for Controller ---
    add_item_requested = pyqtSignal()
    delete_item_requested = pyqtSignal(str) 
    search_requested = pyqtSignal(str)
    clear_search_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("校园咸鱼 V1.0 - Marketplace")
        self.setGeometry(200, 200, 900, 700) # Increased size
        
        # Load Styles
        self._load_styles()

        self._selected_item_id: Optional[str] = None
        self._cards: Dict[str, ItemCard] = {} # Map item_id -> ItemCard widget

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

        # --- Top Bar: Title & Search ---
        top_bar = QHBoxLayout()
        
        title_label = QLabel("Campus Xianyu")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        top_bar.addWidget(title_label)
        
        top_bar.addStretch()

        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search items...")
        self.search_input.setFixedWidth(250)
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("PrimaryButton")
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        search_layout.addWidget(self.search_button)
        
        self.clear_search_button = QPushButton("Clear")
        self.clear_search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        search_layout.addWidget(self.clear_search_button)
        
        top_bar.addLayout(search_layout)
        main_layout.addLayout(top_bar)

        # --- Content Area: Scrollable Card Grid ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ScrollContents")
        # Use FlowLayout for responsive grid
        self.flow_layout = FlowLayout(self.scroll_content, margin=10, h_spacing=20, v_spacing=20) 
        
        scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(scroll_area)

        # --- Bottom Bar: Actions ---
        action_layout = QHBoxLayout()
        
        self.add_button = QPushButton("+ Sell New Item")
        self.add_button.setObjectName("PrimaryButton")
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.setMinimumHeight(40)
        action_layout.addWidget(self.add_button)
        
        action_layout.addStretch()
        
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setEnabled(False) 
        self.delete_button.setMinimumHeight(40)
        self.delete_button.setStyleSheet("color: #E74C3C; border-color: #E74C3C;")
        action_layout.addWidget(self.delete_button)
        
        main_layout.addLayout(action_layout)

        # --- Connections ---
        self.add_button.clicked.connect(self.add_item_requested)
        self.search_button.clicked.connect(self.on_search_clicked)
        self.search_input.returnPressed.connect(self.on_search_clicked)
        self.clear_search_button.clicked.connect(self.on_clear_search_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)

    # --- Private Slots ---

    def on_card_clicked(self, item_id: str):
        """Handle card selection logic."""
        # Deselect previous
        if self._selected_item_id and self._selected_item_id in self._cards:
            self._cards[self._selected_item_id].set_selected(False)
        
        # Select new
        self._selected_item_id = item_id
        if item_id in self._cards:
            self._cards[item_id].set_selected(True)
            
        self.delete_button.setEnabled(True)

    def on_search_clicked(self):
        term = self.get_search_term()
        self.search_requested.emit(term)
        
    def on_clear_search_clicked(self):
        self.clear_search_input()
        self.clear_search_requested.emit()

    def on_delete_clicked(self):
        if self._selected_item_id:
            self.delete_item_requested.emit(self._selected_item_id)

    # --- Public Methods for Controller ---

    def update_view(self, items: List[Dict[str, str]]):
        """
        Refresh the grid of cards.
        """
        # Clear existing layout items
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self._cards.clear()
        self._selected_item_id = None
        self.delete_button.setEnabled(False)

        for item in items:
            card = ItemCard(
                item_id=item['id'],
                name=item['name'],
                description=item['description'],
                contact=item['contact_info']
            )
            # Connect card click signal
            card.clicked.connect(self.on_card_clicked)
            
            self.flow_layout.addWidget(card)
            self._cards[item['id']] = card

    def get_search_term(self) -> str:
        return self.search_input.text().strip()
    
    def clear_search_input(self):
        self.search_input.clear()

    def get_selected_item_name(self) -> Optional[str]:
        if self._selected_item_id and self._selected_item_id in self._cards:
            # We can retrieve the name from the card label or by storing data map.
            # Here we just read the card's name label for simplicity
            return self._cards[self._selected_item_id].lbl_name.text()
        return None
