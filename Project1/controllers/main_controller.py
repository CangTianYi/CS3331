# controllers/main_controller.py
# 切换到 PyQt5: from PyQt5.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject # Controller 可以是 QObject 

from model.data_manager import CsvDataManager
from views.main_window import MainWindow
from views.add_item_dialog import AddItemDialog

class MainController(QObject):
    """
    PRD 4.3: Controller (控制层)
    连接 View (视图) 和 Model (数据)。
    处理按钮点击事件，调用 CsvDataManager 的方法，并更新 View。
    """
    def __init__(self):
        super().__init__()
        
        # PRD 4.3: 实例化 M 和 V
        self.model = CsvDataManager()
        self.view = MainWindow()

        # --- 核心：连接 View 的信号(signals) 到 Controller 的槽(slots) ---
        self.view.add_item_requested.connect(self.show_add_item_dialog)
        self.view.delete_item_requested.connect(self.handle_delete_item)
        self.view.search_requested.connect(self.handle_search)
        self.view.clear_search_requested.connect(self.handle_clear_search)

        # 初始加载数据
        self.refresh_table_view()

    def run(self):
        """启动应用，显示主窗口。"""
        self.view.show()

    def refresh_table_view(self):
        """从模型加载所有数据并更新视图。"""
        all_items = self.model.get_all_items()
        self.view.update_table(all_items)

    # --- 槽函数 (Slots) ---

    def show_add_item_dialog(self):
        """
        处理 FR-002: 添加物品
        """
        # 创建并显示对话框
        dialog = AddItemDialog(self.view)
        
        # .exec() 会阻塞，直到对话框关闭
        if dialog.exec(): # QDialog.DialogCode.Accepted (用户点击了"保存"且校验通过)
            data = dialog.get_data()
            
            # 1. 调用 Model 添加数据
            self.model.add_item(
                name=data["name"],
                description=data["description"],
                contact_info=data["contact"]
            )
            
            # 2. PRD 4.2.2: 立即将内存列表写回 CSV
            self.model.save_data()
            
            # 3. FR-001: 刷新主界面的物品列表
            self.refresh_table_view()

    def handle_delete_item(self, item_id: str):
        """
        处理 FR-003: 删除物品
        """
        item_name = self.view.get_selected_item_name() or "该物品"

        # PRD 3.3: 安全确认
        reply = QMessageBox.warning(
            self.view,
            "确认删除", # 标题
            f"您确定要删除「{item_name}」吗？\n此操作不可撤销。", # 内容
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No # 默认焦点在 "No"
        )

        if reply == QMessageBox.StandardButton.Yes:
            # 1. 调用 Model 删除
            deleted = self.model.delete_item(item_id)
            
            if deleted:
                # 2. PRD 4.2.2: 立即写回
                self.model.save_data()
                # 3. FR-001: 刷新列表
                self.refresh_table_view()
            else:
                # 理论上不应该发生，因为 ID 来自 UI
                QMessageBox.critical(self.view, "错误", "删除失败：未在数据中找到该物品。")

    def handle_search(self, keyword: str):
        """
        处理 FR-004: 查找物品
        """
        if not keyword:
            self.refresh_table_view()
            return
        
        # 1. 调用 Model 在内存中搜索
        results = self.model.search_items(keyword)
        
        # 2. FR-001: 列表应刷新，仅显示结果
        self.view.update_table(results)

    def handle_clear_search(self):
        """
        处理 FR-004: 清除/重置
        """
        # 注意：View 已经自己清除了输入框 (在 on_clear_search_clicked 中)
        # 我们只需要刷新列表以显示所有物品
        self.refresh_table_view()