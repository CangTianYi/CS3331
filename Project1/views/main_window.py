# views/main_window.py
# 切换到 PyQt5: from PyQt5.QtWidgets import ...; from PyQt5.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QAbstractItemView, QHeaderView, QLabel, QTableWidgetItem
)
from PyQt6.QtCore import pyqtSignal, Qt

class MainWindow(QWidget):
    """
    PRD 3.1: 主窗口 (View)
    只负责 UI 布局和显示，通过 signals (信号) 与 Controller 通信。
    """
    
    # --- 为 Controller 定义的信号 ---
    # 当用户点击 "添加" 按钮时发出
    add_item_requested = pyqtSignal()
    # 当用户确认 "删除" 按钮时发出，携带要删除的 item_id
    delete_item_requested = pyqtSignal(str) 
    # 当用户点击 "搜索" 按钮时发出，携带关键词
    search_requested = pyqtSignal(str)
    # 当用户点击 "清除" 按钮时发出
    clear_search_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("校园咸鱼 V1.0")
        self.setGeometry(200, 200, 700, 500) # x, y, width, height
        
        # 内部映射，用于根据表格行号查找真实的 data 'id'
        # [ { 'id': 'uuid1', 'name': '...' }, ... ]
        self._table_item_ids: List[str] = []

        self.setup_ui()

    def setup_ui(self):
        # PRD 3.1: 垂直流式布局
        main_layout = QVBoxLayout(self)

        # --- PRD 3.1: 顶部区域 (工具栏/搜索) ---
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("搜索："))
        
        # PRD FR-004: 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索物品名称或描述...")
        search_layout.addWidget(self.search_input)
        
        # PRD FR-004: 搜索按钮
        self.search_button = QPushButton("搜索")
        search_layout.addWidget(self.search_button)
        
        # PRD FR-004: 清除按钮
        self.clear_search_button = QPushButton("清除搜索")
        search_layout.addWidget(self.clear_search_button)
        
        main_layout.addLayout(search_layout)

        # --- PRD 3.1: 中部区域 (内容区) ---
        # PRD 3.1: 使用 QTableWidget
        self.table_widget = QTableWidget()
        # PRD 3.1: 表格列
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["物品名称", "物品描述", "联系人信息"])
        
        # --- UI/UX 优化 (符合 PRD 简洁风格) ---
        # PRD FR-003: 必须能够选中一个物品 (设置为选中整行)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # 仅允许单选
        self.table_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # 禁止编辑
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # 隐藏垂直表头 (行号)
        self.table_widget.verticalHeader().setVisible(False)
        # 允许排序
        self.table_widget.setSortingEnabled(True)
        
        # PRD 3.1: 列宽设置
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive) # 名称可拖动
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # 描述自适应
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive) # 联系人可拖动
        
        # PRD FR-001: 占据主要空间
        main_layout.addWidget(self.table_widget)

        # --- PRD 3.1: 底部区域 (操作栏) ---
        action_layout = QHBoxLayout()
        
        # PRD FR-002: 添加按钮
        self.add_button = QPushButton("添加新物品...")
        action_layout.addWidget(self.add_button)
        
        # PRD FR-003: 删除按钮
        self.delete_button = QPushButton("删除选中物品")
        # PRD 3.1: 默认禁用
        self.delete_button.setEnabled(False) 
        action_layout.addWidget(self.delete_button)
        
        action_layout.addStretch() # 将按钮推向左侧
        main_layout.addLayout(action_layout)

        # --- 内部信号与槽的连接 ---
        # 当表格选择变化时，更新 "删除" 按钮的状态
        self.table_widget.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        # --- 连接 View 控件到 "pyqtSignal" ---
        # (Controller 将会监听这些 pyqtSignal)
        self.add_button.clicked.connect(self.add_item_requested)
        self.search_button.clicked.connect(self.on_search_clicked)
        # PRD FR-004: 支持回车搜索
        self.search_input.returnPressed.connect(self.on_search_clicked)
        self.clear_search_button.clicked.connect(self.on_clear_search_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)

    # --- 内部槽函数 (Private Slots) ---

    def on_selection_changed(self):
        """PRD 3.1: 选中列表项后激活 (删除按钮)。"""
        # 检查是否有任何项被选中
        is_item_selected = bool(self.table_widget.selectionModel().selectedRows())
        self.delete_button.setEnabled(is_item_selected)

    def on_search_clicked(self):
        """当点击搜索或按回车时，发出 search_requested 信号。"""
        term = self.get_search_term()
        self.search_requested.emit(term)
        
    def on_clear_search_clicked(self):
        """当点击清除时，清空输入框并发出 clear_search_requested 信号。"""
        self.clear_search_input()
        self.clear_search_requested.emit()

    def on_delete_clicked(self):
        """当点击删除时，获取选中项的 ID，并发出 delete_item_requested 信号。"""
        item_id = self.get_selected_item_id()
        if item_id:
            self.delete_item_requested.emit(item_id)

    # --- 公共方法 (Public Methods for Controller) ---

    def update_table(self, items: List[Dict[str, str]]):
        """
        FR-001: 物品列表展示。
        由 Controller 调用，用传入的数据刷新表格。
        """
        # 暂时禁用排序以提高插入性能
        self.table_widget.setSortingEnabled(False)
        
        self.table_widget.setRowCount(0) # 清空表格
        self._table_item_ids = [] # 清空 ID 映射
        
        for item in items:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            
            # PRD 4.2.3: 存储 ID 用于删除 (但不显示)
            self._table_item_ids.append(item['id'])
            
            # 填充表格 (PRD FR-001: 名称, 描述, 联系人)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(item['name']))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(item['description']))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(item['contact_info']))

        # 重新启用排序
        self.table_widget.setSortingEnabled(True)
        # 刷新后，选择被清除，确保删除按钮被禁用
        self.on_selection_changed()

    def get_search_term(self) -> str:
        """获取搜索框中的文本。"""
        return self.search_input.text().strip()
    
    def clear_search_input(self):
        """清空搜索框。"""
        self.search_input.clear()

    def get_selected_item_id(self) -> Optional[str]:
        """获取当前选中行的物品 ID。"""
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return None
        
        selected_row_index = selected_rows[0].row() # 我们是单选
        if 0 <= selected_row_index < len(self._table_item_ids):
            return self._table_item_ids[selected_row_index]
        return None

    def get_selected_item_name(self) -> Optional[str]:
        """获取当前选中行的物品名称 (用于删除确认框)。"""
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return None
        
        name_item = self.table_widget.item(selected_rows[0].row(), 0)
        if name_item:
            return name_item.text()
        return None