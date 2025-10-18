# model/data_manager.py
import csv
import os
import uuid
from typing import List, Dict, Optional
from config import ITEMS_CSV_PATH, CSV_HEADERS

class CsvDataManager:
    """
    PRD 4.3: Model (数据模型层)
    负责处理 items.csv 的所有读写逻辑。
    完全独立于 UI (PyQt)。
    """
    def __init__(self):
        self.data_file = ITEMS_CSV_PATH
        self.headers = CSV_HEADERS
        # PRD 4.2.2: 内存中的数据列表 (List of Dictionaries)
        self._items_cache: List[Dict[str, str]] = []
        
        self._initialize_data_file()
        self.load_data()

    def _initialize_data_file(self):
        """如果 items.csv 不存在，则创建它并写入表头。"""
        if not os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # PRD 4.2: 写入数据列 (Headers)
                    writer.writerow(self.headers)
            except IOError as e:
                print(f"Error initializing data file {self.data_file}: {e}")
                # 在实际应用中，这里应该向用户显示一个错误
    
    def load_data(self):
        """
        PRD 4.2.2: 读取 (Load)
        程序启动时，一次性将 CSV 读入内存中的 _items_cache。
        """
        self._items_cache = []
        try:
            with open(self.data_file, 'r', newline='', encoding='utf-8') as f:
                # PRD 4.2.2: 必须使用 csv.DictReader
                reader = csv.DictReader(f)
                
                # 健全性检查：确保表头匹配
                if reader.fieldnames != self.headers:
                    print(f"Warning: CSV header mismatch. Re-initializing file.")
                    # 如果表头损坏或不匹配，则重建文件
                    self._initialize_data_file()
                    return

                for row in reader:
                    self._items_cache.append(row)
        except FileNotFoundError:
            print("Data file not found. Creating a new one.")
            self._initialize_data_file()
        except Exception as e:
            print(f"Error loading data: {e}")
            # 此处应有更健壮的错误处理

    def save_data(self):
        """
        PRD 4.2.2: 写入 (Save)
        将完整的内存列表 (_items_cache) 覆盖写回 (Overwrite) items.csv 文件。
        """
        try:
            with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
                # PRD 4.2.2: 必须使用 csv.DictWriter
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(self._items_cache)
        except IOError as e:
            print(f"Error saving data: {e}")
            # 此处应向用户显示保存失败的错误

    def get_all_items(self) -> List[Dict[str, str]]:
        """获取内存中的所有物品列表。"""
        return self._items_cache

    def add_item(self, name: str, description: str, contact_info: str) -> Dict[str, str]:
        """
        FR-002: 添加物品
        PRD 4.2.1: ID的生成 (使用 UUID)
        """
        new_id = uuid.uuid4().hex
        new_item = {
            'id': new_id,
            'name': name,
            'description': description,
            'contact_info': contact_info
        }
        # 1. 更新内存列表
        self._items_cache.append(new_item)
        # 2. Controller 将负责调用 save_data() 来持久化
        return new_item

    def delete_item(self, item_id: str) -> bool:
        """
        FR-003 & PRD 4.2.3: 删除操作
        从内存列表中移除指定 id 的项。
        """
        item_to_delete = None
        for item in self._items_cache:
            if item['id'] == item_id:
                item_to_delete = item
                break
        
        if item_to_delete:
            # 1. 从内存列表中移除
            self._items_cache.remove(item_to_delete)
            # 2. Controller 将负责调用 save_data()
            return True
        
        return False # 未找到该 ID

    def search_items(self, keyword: str) -> List[Dict[str, str]]:
        """
        FR-004 & PRD 4.2.4: 搜索操作
        在内存中筛选 name 或 description 包含关键词的项。
        """
        if not keyword:
            return self.get_all_items()
        
        keyword_lower = keyword.lower()
        results = []
        for item in self._items_cache:
            # PRD 4.0: 模糊匹配
            name_match = keyword_lower in item['name'].lower()
            desc_match = keyword_lower in item['description'].lower()
            if name_match or desc_match:
                results.append(item)
        return results