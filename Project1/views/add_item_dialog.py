# views/add_item_dialog.py
# �л��� PyQt5: from PyQt5.QtWidgets import ...
from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QTextEdit, QPushButton, QFormLayout, 
    QVBoxLayout, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt

class AddItemDialog(QDialog):
    """
    PRD 3.2: �����Ʒ�Ի��� (View)
    ����һ��ģʽ�Ի��� (QDialog)��ֻ���� UI ���ֺͻ�ȡ�û����롣
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("�������Ʒ")
        # PRD FR-002: ģʽ�Ի���
        self.setModal(True)
        self.setMinimumWidth(350)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # PRD 3.2: ������ (QFormLayout)
        form_layout = QFormLayout()

        # PRD 3.2: �ؼ�
        self.name_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.contact_edit = QLineEdit()
        
        # PRD FR-002: ��ʾ������
        form_layout.addRow("��Ʒ���� (*):", self.name_edit)
        form_layout.addRow("��Ʒ����:", self.desc_edit)
        form_layout.addRow("��ϵ��Ϣ (*):", self.contact_edit)

        layout.addLayout(form_layout)

        # PRD 3.2: �ײ���ť (ʹ�ñ�׼��ť��)
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText("����")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("ȡ��")

        # ���� "����" �� "ȡ��" �ź�
        self.button_box.accepted.connect(self.accept) # ���õ� "accept"
        self.button_box.rejected.connect(self.reject) # ���õ� "reject"

        layout.addWidget(self.button_box)

    def get_data(self) -> dict:
        """�����������ӱ��ؼ��л�ȡ���ݡ�"""
        return {
            "name": self.name_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip(),
            "contact": self.contact_edit.text().strip()
        }

    def validate_input(self) -> bool:
        """PRD FR-002: У������"""
        data = self.get_data()
        if not data["name"] or not data["contact"]:
            return False
        return True

    # ��д accept() �������� "����" ʱ����У��
    def accept(self):
        if self.validate_input():
            # У��ͨ�������ø���� accept()���رնԻ��򲢷��� QDialog.DialogCode.Accepted
            super().accept()
        else:
            # У��ʧ�ܣ���ʾ���棬���رնԻ���
            QMessageBox.warning(
                self, 
                "��Ϣ������", 
                "����Ʒ���ơ��͡���ϵ��Ϣ���Ǳ����"
            )