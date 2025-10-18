# views/add_item_dialog.py
# 切换到 PyQt5: from PyQt5.QtWidgets import ...
from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QTextEdit, QPushButton, QFormLayout, 
    QVBoxLayout, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt

class AddItemDialog(QDialog):
    """
    PRD 3.2: 添加物品对话框 (View)
    这是一个模式对话框 (QDialog)，只负责 UI 布局和获取用户输入。
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加新物品")
        # PRD FR-002: 模式对话框
        self.setModal(True)
        self.setMinimumWidth(350)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # PRD 3.2: 表单布局 (QFormLayout)
        form_layout = QFormLayout()

        # PRD 3.2: 控件
        self.name_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.contact_edit = QLineEdit()
        
        # PRD FR-002: 提示必填项
        form_layout.addRow("物品名称 (*):", self.name_edit)
        form_layout.addRow("物品描述:", self.desc_edit)
        form_layout.addRow("联系信息 (*):", self.contact_edit)

        layout.addLayout(form_layout)

        # PRD 3.2: 底部按钮 (使用标准按钮盒)
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText("保存")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("取消")

        # 连接 "保存" 和 "取消" 信号
        self.button_box.accepted.connect(self.accept) # 内置的 "accept"
        self.button_box.rejected.connect(self.reject) # 内置的 "reject"

        layout.addWidget(self.button_box)

    def get_data(self) -> dict:
        """辅助方法：从表单控件中获取数据。"""
        return {
            "name": self.name_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip(),
            "contact": self.contact_edit.text().strip()
        }

    def validate_input(self) -> bool:
        """PRD FR-002: 校验必填项。"""
        data = self.get_data()
        if not data["name"] or not data["contact"]:
            return False
        return True

    # 重写 accept() 方法以在 "保存" 时加入校验
    def accept(self):
        if self.validate_input():
            # 校验通过，调用父类的 accept()，关闭对话框并返回 QDialog.DialogCode.Accepted
            super().accept()
        else:
            # 校验失败，显示警告，不关闭对话框
            QMessageBox.warning(
                self, 
                "信息不完整", 
                "“物品名称”和“联系信息”是必填项。"
            )