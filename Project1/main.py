# main.py
import sys
# �л��� PyQt5: from PyQt5.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication

from controllers.main_controller import MainController

if __name__ == "__main__":
    # 1. ���� QApplication ʵ��
    app = QApplication(sys.argv)
    
    # 2. PRD 4.3: ʵ���� Controller
    # Controller ������ʵ���� Model �� View
    controller = MainController()
    
    # 3. ���� Controller (���Ḻ����ʾ View)
    controller.run()
    
    # 4. ����Ӧ�ó�����¼�ѭ��
    sys.exit(app.exec())