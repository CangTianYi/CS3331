899
# main.py
"""
Campus Xianyu - Campus Second-hand Item Revival System
Entry point for the application.
"""
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtCore import QFile, QTextStream

from controllers.main_controller import MainController

def load_global_styles(app: QApplication):
    """Load global stylesheet."""
    style_path = os.path.join(os.path.dirname(__file__), "assets", "styles.qss")
    file = QFile(style_path)
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

if __name__ == "__main__":
    # 1. Create QApplication instance
    app = QApplication(sys.argv)
    
    # 2. Load global styles
    load_global_styles(app)
    
    # 3. Create main stacked widget (acts as the window container)
    stack = QStackedWidget()
    stack.setWindowTitle("Campus Xianyu")
    stack.setGeometry(150, 150, 1100, 800)
    
    # 4. Create and run the main controller
    controller = MainController(stack)
    controller.run()
    
    # 5. Start the event loop
    sys.exit(app.exec())