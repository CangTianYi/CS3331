# model/data_manager.py
import csv
import os
import uuid
from typing import List, Dict, Optional
from config import ITEMS_CSV_PATH, CSV_HEADERS

class CsvDataManager:
    """
    PRD 4.3: Model (����ģ�Ͳ�)
    ������ items.csv �����ж�д�߼���
    ��ȫ������ UI (PyQt)��
    """
    def __init__(self):
        self.data_file = ITEMS_CSV_PATH
        self.headers = CSV_HEADERS
        # PRD 4.2.2: �ڴ��е������б� (List of Dictionaries)
        self._items_cache: List[Dict[str, str]] = []
        
        self._initialize_data_file()
        self.load_data()

    def _initialize_data_file(self):
        """��� items.csv �����ڣ��򴴽�����д���ͷ��"""
        if not os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # PRD 4.2: д�������� (Headers)
                    writer.writerow(self.headers)
            except IOError as e:
                print(f"Error initializing data file {self.data_file}: {e}")
                # ��ʵ��Ӧ���У�����Ӧ�����û���ʾһ������
    
    def load_data(self):
        """
        PRD 4.2.2: ��ȡ (Load)
        ��������ʱ��һ���Խ� CSV �����ڴ��е� _items_cache��
        """
        self._items_cache = []
        try:
            with open(self.data_file, 'r', newline='', encoding='utf-8') as f:
                # PRD 4.2.2: ����ʹ�� csv.DictReader
                reader = csv.DictReader(f)
                
                # ��ȫ�Լ�飺ȷ����ͷƥ��
                if reader.fieldnames != self.headers:
                    print(f"Warning: CSV header mismatch. Re-initializing file.")
                    # �����ͷ�𻵻�ƥ�䣬���ؽ��ļ�
                    self._initialize_data_file()
                    return

                for row in reader:
                    self._items_cache.append(row)
        except FileNotFoundError:
            print("Data file not found. Creating a new one.")
            self._initialize_data_file()
        except Exception as e:
            print(f"Error loading data: {e}")
            # �˴�Ӧ�и���׳�Ĵ�����

    def save_data(self):
        """
        PRD 4.2.2: д�� (Save)
        ���������ڴ��б� (_items_cache) ����д�� (Overwrite) items.csv �ļ���
        """
        try:
            with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
                # PRD 4.2.2: ����ʹ�� csv.DictWriter
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(self._items_cache)
        except IOError as e:
            print(f"Error saving data: {e}")
            # �˴�Ӧ���û���ʾ����ʧ�ܵĴ���

    def get_all_items(self) -> List[Dict[str, str]]:
        """��ȡ�ڴ��е�������Ʒ�б�"""
        return self._items_cache

    def add_item(self, name: str, description: str, contact_info: str) -> Dict[str, str]:
        """
        FR-002: �����Ʒ
        PRD 4.2.1: ID������ (ʹ�� UUID)
        """
        new_id = uuid.uuid4().hex
        new_item = {
            'id': new_id,
            'name': name,
            'description': description,
            'contact_info': contact_info
        }
        # 1. �����ڴ��б�
        self._items_cache.append(new_item)
        # 2. Controller ��������� save_data() ���־û�
        return new_item

    def delete_item(self, item_id: str) -> bool:
        """
        FR-003 & PRD 4.2.3: ɾ������
        ���ڴ��б����Ƴ�ָ�� id ���
        """
        item_to_delete = None
        for item in self._items_cache:
            if item['id'] == item_id:
                item_to_delete = item
                break
        
        if item_to_delete:
            # 1. ���ڴ��б����Ƴ�
            self._items_cache.remove(item_to_delete)
            # 2. Controller ��������� save_data()
            return True
        
        return False # δ�ҵ��� ID

    def search_items(self, keyword: str) -> List[Dict[str, str]]:
        """
        FR-004 & PRD 4.2.4: ��������
        ���ڴ���ɸѡ name �� description �����ؼ��ʵ��
        """
        if not keyword:
            return self.get_all_items()
        
        keyword_lower = keyword.lower()
        results = []
        for item in self._items_cache:
            # PRD 4.0: ģ��ƥ��
            name_match = keyword_lower in item['name'].lower()
            desc_match = keyword_lower in item['description'].lower()
            if name_match or desc_match:
                results.append(item)
        return results