# views/main_window.py
# �л��� PyQt5: from PyQt5.QtWidgets import ...; from PyQt5.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QAbstractItemView, QHeaderView, QLabel, QTableWidgetItem
)
from PyQt6.QtCore import pyqtSignal, Qt

class MainWindow(QWidget):
    """
    PRD 3.1: ������ (View)
    ֻ���� UI ���ֺ���ʾ��ͨ�� signals (�ź�) �� Controller ͨ�š�
    """
    
    # --- Ϊ Controller ������ź� ---
    # ���û���� "���" ��ťʱ����
    add_item_requested = pyqtSignal()
    # ���û�ȷ�� "ɾ��" ��ťʱ������Я��Ҫɾ���� item_id
    delete_item_requested = pyqtSignal(str) 
    # ���û���� "����" ��ťʱ������Я���ؼ���
    search_requested = pyqtSignal(str)
    # ���û���� "���" ��ťʱ����
    clear_search_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("У԰���� V1.0")
        self.setGeometry(200, 200, 700, 500) # x, y, width, height
        
        # �ڲ�ӳ�䣬���ڸ��ݱ���кŲ�����ʵ�� data 'id'
        # [ { 'id': 'uuid1', 'name': '...' }, ... ]
        self._table_item_ids: List[str] = []

        self.setup_ui()

    def setup_ui(self):
        # PRD 3.1: ��ֱ��ʽ����
        main_layout = QVBoxLayout(self)

        # --- PRD 3.1: �������� (������/����) ---
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("������"))
        
        # PRD FR-004: ������
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("������Ʒ���ƻ�����...")
        search_layout.addWidget(self.search_input)
        
        # PRD FR-004: ������ť
        self.search_button = QPushButton("����")
        search_layout.addWidget(self.search_button)
        
        # PRD FR-004: �����ť
        self.clear_search_button = QPushButton("�������")
        search_layout.addWidget(self.clear_search_button)
        
        main_layout.addLayout(search_layout)

        # --- PRD 3.1: �в����� (������) ---
        # PRD 3.1: ʹ�� QTableWidget
        self.table_widget = QTableWidget()
        # PRD 3.1: �����
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["��Ʒ����", "��Ʒ����", "��ϵ����Ϣ"])
        
        # --- UI/UX �Ż� (���� PRD �����) ---
        # PRD FR-003: �����ܹ�ѡ��һ����Ʒ (����Ϊѡ������)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # ������ѡ
        self.table_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # ��ֹ�༭
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # ���ش�ֱ��ͷ (�к�)
        self.table_widget.verticalHeader().setVisible(False)
        # ��������
        self.table_widget.setSortingEnabled(True)
        
        # PRD 3.1: �п�����
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive) # ���ƿ��϶�
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # ��������Ӧ
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive) # ��ϵ�˿��϶�
        
        # PRD FR-001: ռ����Ҫ�ռ�
        main_layout.addWidget(self.table_widget)

        # --- PRD 3.1: �ײ����� (������) ---
        action_layout = QHBoxLayout()
        
        # PRD FR-002: ��Ӱ�ť
        self.add_button = QPushButton("�������Ʒ...")
        action_layout.addWidget(self.add_button)
        
        # PRD FR-003: ɾ����ť
        self.delete_button = QPushButton("ɾ��ѡ����Ʒ")
        # PRD 3.1: Ĭ�Ͻ���
        self.delete_button.setEnabled(False) 
        action_layout.addWidget(self.delete_button)
        
        action_layout.addStretch() # ����ť�������
        main_layout.addLayout(action_layout)

        # --- �ڲ��ź���۵����� ---
        # �����ѡ��仯ʱ������ "ɾ��" ��ť��״̬
        self.table_widget.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        # --- ���� View �ؼ��� "pyqtSignal" ---
        # (Controller ���������Щ pyqtSignal)
        self.add_button.clicked.connect(self.add_item_requested)
        self.search_button.clicked.connect(self.on_search_clicked)
        # PRD FR-004: ֧�ֻس�����
        self.search_input.returnPressed.connect(self.on_search_clicked)
        self.clear_search_button.clicked.connect(self.on_clear_search_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)

    # --- �ڲ��ۺ��� (Private Slots) ---

    def on_selection_changed(self):
        """PRD 3.1: ѡ���б���󼤻� (ɾ����ť)��"""
        # ����Ƿ����κ��ѡ��
        is_item_selected = bool(self.table_widget.selectionModel().selectedRows())
        self.delete_button.setEnabled(is_item_selected)

    def on_search_clicked(self):
        """����������򰴻س�ʱ������ search_requested �źš�"""
        term = self.get_search_term()
        self.search_requested.emit(term)
        
    def on_clear_search_clicked(self):
        """��������ʱ���������򲢷��� clear_search_requested �źš�"""
        self.clear_search_input()
        self.clear_search_requested.emit()

    def on_delete_clicked(self):
        """�����ɾ��ʱ����ȡѡ����� ID�������� delete_item_requested �źš�"""
        item_id = self.get_selected_item_id()
        if item_id:
            self.delete_item_requested.emit(item_id)

    # --- �������� (Public Methods for Controller) ---

    def update_table(self, items: List[Dict[str, str]]):
        """
        FR-001: ��Ʒ�б�չʾ��
        �� Controller ���ã��ô��������ˢ�±��
        """
        # ��ʱ������������߲�������
        self.table_widget.setSortingEnabled(False)
        
        self.table_widget.setRowCount(0) # ��ձ��
        self._table_item_ids = [] # ��� ID ӳ��
        
        for item in items:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            
            # PRD 4.2.3: �洢 ID ����ɾ�� (������ʾ)
            self._table_item_ids.append(item['id'])
            
            # ����� (PRD FR-001: ����, ����, ��ϵ��)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(item['name']))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(item['description']))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(item['contact_info']))

        # ������������
        self.table_widget.setSortingEnabled(True)
        # ˢ�º�ѡ�������ȷ��ɾ����ť������
        self.on_selection_changed()

    def get_search_term(self) -> str:
        """��ȡ�������е��ı���"""
        return self.search_input.text().strip()
    
    def clear_search_input(self):
        """���������"""
        self.search_input.clear()

    def get_selected_item_id(self) -> Optional[str]:
        """��ȡ��ǰѡ���е���Ʒ ID��"""
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return None
        
        selected_row_index = selected_rows[0].row() # �����ǵ�ѡ
        if 0 <= selected_row_index < len(self._table_item_ids):
            return self._table_item_ids[selected_row_index]
        return None

    def get_selected_item_name(self) -> Optional[str]:
        """��ȡ��ǰѡ���е���Ʒ���� (����ɾ��ȷ�Ͽ�)��"""
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return None
        
        name_item = self.table_widget.item(selected_rows[0].row(), 0)
        if name_item:
            return name_item.text()
        return None