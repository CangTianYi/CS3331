# config.py
import os

# ������Ŀ��Ŀ¼
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PRD 4.2: ���ݴ洢�� items.csv
ITEMS_CSV_PATH = os.path.join(BASE_DIR, "items.csv")

# PRD 4.2: CSV �ļ��淶
CSV_HEADERS = ['id', 'name', 'description', 'contact_info']