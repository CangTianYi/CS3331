# -*- coding: utf-8 -*-
# model/item_type_manager.py
"""
Item Type Management: Create, Update, Delete item categories.
"""
import json
from model.database import db

class ItemTypeManager:
    """Handles item type (category) database operations."""

    def create_type(self, name: str, custom_attributes: list) -> dict:
        """Create a new item type."""
        try:
            type_id = db.execute_query(
                "INSERT INTO item_types (name, custom_attributes) VALUES (?, ?)",
                (name, json.dumps(custom_attributes))
            )
            return {'id': type_id, 'name': name, 'custom_attributes': custom_attributes}
        except Exception as e:
            if 'UNIQUE constraint' in str(e):
                return None
            raise

    def update_type(self, type_id: int, name: str, custom_attributes: list) -> bool:
        """Update an existing item type."""
        db.execute_query(
            "UPDATE item_types SET name = ?, custom_attributes = ? WHERE id = ?",
            (name, json.dumps(custom_attributes), type_id)
        )
        return True

    def delete_type(self, type_id: int) -> bool:
        """Delete an item type."""
        db.execute_query(
            "DELETE FROM item_types WHERE id = ?",
            (type_id,)
        )
        return True

    def get_all_types(self) -> list:
        """Get all item types."""
        types = db.execute_query(
            "SELECT * FROM item_types ORDER BY name",
            fetch=True
        )
        for t in types:
            if isinstance(t['custom_attributes'], str):
                t['custom_attributes'] = json.loads(t['custom_attributes'])
            elif t['custom_attributes'] is None:
                t['custom_attributes'] = []
        return types

    def get_type_by_id(self, type_id: int) -> dict:
        """Get a single item type by ID."""
        item_type = db.execute_query(
            "SELECT * FROM item_types WHERE id = ?",
            (type_id,),
            fetchone=True
        )
        if item_type:
            if isinstance(item_type['custom_attributes'], str):
                item_type['custom_attributes'] = json.loads(item_type['custom_attributes'])
            elif item_type['custom_attributes'] is None:
                item_type['custom_attributes'] = []
        return item_type
