# controllers/main_controller.py
# �л��� PyQt5: from PyQt5.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject # Controller ������ QObject 

from model.data_manager import CsvDataManager
from views.main_window import MainWindow
from views.add_item_dialog import AddItemDialog

class MainController(QObject):
    """
    PRD 4.3: Controller (���Ʋ�)
    ���� View (��ͼ) �� Model (����)��
    ����ť����¼������� CsvDataManager �ķ����������� View��
    """
    def __init__(self):
        super().__init__()
        
        # PRD 4.3: ʵ���� M �� V
        self.model = CsvDataManager()
        self.view = MainWindow()

        # --- ���ģ����� View ���ź�(signals) �� Controller �Ĳ�(slots) ---
        self.view.add_item_requested.connect(self.show_add_item_dialog)
        self.view.delete_item_requested.connect(self.handle_delete_item)
        self.view.search_requested.connect(self.handle_search)
        self.view.clear_search_requested.connect(self.handle_clear_search)

        # ��ʼ��������
        self.refresh_table_view()

    def run(self):
        """����Ӧ�ã���ʾ�����ڡ�"""
        self.view.show()

    def refresh_table_view(self):
        """��ģ�ͼ����������ݲ�������ͼ��"""
        all_items = self.model.get_all_items()
        self.view.update_table(all_items)

    # --- �ۺ��� (Slots) ---

    def show_add_item_dialog(self):
        """
        ���� FR-002: �����Ʒ
        """
        # ��������ʾ�Ի���
        dialog = AddItemDialog(self.view)
        
        # .exec() ��������ֱ���Ի���ر�
        if dialog.exec(): # QDialog.DialogCode.Accepted (�û������"����"��У��ͨ��)
            data = dialog.get_data()
            
            # 1. ���� Model �������
            self.model.add_item(
                name=data["name"],
                description=data["description"],
                contact_info=data["contact"]
            )
            
            # 2. PRD 4.2.2: �������ڴ��б�д�� CSV
            self.model.save_data()
            
            # 3. FR-001: ˢ�����������Ʒ�б�
            self.refresh_table_view()

    def handle_delete_item(self, item_id: str):
        """
        ���� FR-003: ɾ����Ʒ
        """
        item_name = self.view.get_selected_item_name() or "����Ʒ"

        # PRD 3.3: ��ȫȷ��
        reply = QMessageBox.warning(
            self.view,
            "ȷ��ɾ��", # ����
            f"��ȷ��Ҫɾ����{item_name}����\n�˲������ɳ�����", # ����
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No # Ĭ�Ͻ����� "No"
        )

        if reply == QMessageBox.StandardButton.Yes:
            # 1. ���� Model ɾ��
            deleted = self.model.delete_item(item_id)
            
            if deleted:
                # 2. PRD 4.2.2: ����д��
                self.model.save_data()
                # 3. FR-001: ˢ���б�
                self.refresh_table_view()
            else:
                # �����ϲ�Ӧ�÷�������Ϊ ID ���� UI
                QMessageBox.critical(self.view, "����", "ɾ��ʧ�ܣ�δ���������ҵ�����Ʒ��")

    def handle_search(self, keyword: str):
        """
        ���� FR-004: ������Ʒ
        """
        if not keyword:
            self.refresh_table_view()
            return
        
        # 1. ���� Model ���ڴ�������
        results = self.model.search_items(keyword)
        
        # 2. FR-001: �б�Ӧˢ�£�����ʾ���
        self.view.update_table(results)

    def handle_clear_search(self):
        """
        ���� FR-004: ���/����
        """
        # ע�⣺View �Ѿ��Լ����������� (�� on_clear_search_clicked ��)
        # ����ֻ��Ҫˢ���б�����ʾ������Ʒ
        self.refresh_table_view()