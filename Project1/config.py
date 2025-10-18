# config.py
import os

# 定义项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PRD 4.2: 数据存储在 items.csv
ITEMS_CSV_PATH = os.path.join(BASE_DIR, "items.csv")

# PRD 4.2: CSV 文件规范
CSV_HEADERS = ['id', 'name', 'description', 'contact_info']