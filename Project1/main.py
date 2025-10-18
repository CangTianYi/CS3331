# main.py
import sys
# 切换到 PyQt5: from PyQt5.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication

from controllers.main_controller import MainController

if __name__ == "__main__":
    # 1. 创建 QApplication 实例
    app = QApplication(sys.argv)
    
    # 2. PRD 4.3: 实例化 Controller
    # Controller 将负责实例化 Model 和 View
    controller = MainController()
    
    # 3. 运行 Controller (它会负责显示 View)
    controller.run()
    
    # 4. 启动应用程序的事件循环
    sys.exit(app.exec())