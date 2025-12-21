from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent

class ItemCard(QFrame):
    """
    A card widget representing a single item.
    """
    clicked = pyqtSignal(str) # Emits item_id when clicked

    def __init__(self, item_id: str, name: str, description: str, contact: str, parent=None):
        super().__init__(parent)
        self.item_id = item_id
        
        # UI Setup
        self.setFixedSize(220, 280) # Fixed size card
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("ItemCard")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        # Name (Title)
        self.lbl_name = QLabel(name)
        self.lbl_name.setObjectName("CardTitle")
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.lbl_name)

        # Contact (Subtitle)
        self.lbl_contact = QLabel(f"? {contact}")
        self.lbl_contact.setObjectName("CardContact")
        layout.addWidget(self.lbl_contact)

        # Spacer for visual separation
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setObjectName("CardLine")
        layout.addWidget(line)

        # Description (Body)
        self.lbl_desc = QLabel(description)
        self.lbl_desc.setObjectName("CardBody")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # Allow description to expand
        layout.addWidget(self.lbl_desc, 1) 

        self._selected = False

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.item_id)
            super().mousePressEvent(event)

    def set_selected(self, selected: bool):
        self._selected = selected
        self.setProperty("selected", selected)
        # Trigger style update
        self.style().unpolish(self)
        self.style().polish(self)
