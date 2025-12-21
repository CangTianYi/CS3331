# -*- coding: utf-8 -*-
# model/item_manager.py
"""
Item Management: CRUD operations for items with category support.
"""
import json
from model.database import db

class ItemManager:
    """Handles item database operations."""

    def add_item(self, type_id: int, owner_id: int, name: str, description: str,
                 location: str, contact_phone: str, contact_email: str,
                 custom_values: dict, image_path: str = None) -> dict:
        """Add a new item."""
        item_id = db.execute_query(
            """
            INSERT INTO items (type_id, owner_id, name, description, location, 
                               contact_phone, contact_email, image_path, custom_values)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (type_id, owner_id, name, description, location, 
             contact_phone, contact_email, image_path, json.dumps(custom_values))
        )
        return {'id': item_id, 'name': name}

    def get_items_by_type(self, type_id: int) -> list:
        """Get all items of a specific type."""
        items = db.execute_query(
            """
            SELECT i.*, u.username as owner_name, t.name as type_name
            FROM items i
            JOIN users u ON i.owner_id = u.id
            JOIN item_types t ON i.type_id = t.id
            WHERE i.type_id = ?
            ORDER BY i.created_at DESC
            """,
            (type_id,),
            fetch=True
        )
        for item in items:
            if isinstance(item['custom_values'], str):
                item['custom_values'] = json.loads(item['custom_values'])
            elif item['custom_values'] is None:
                item['custom_values'] = {}
        return items

    def get_all_items(self) -> list:
        """Get all items."""
        items = db.execute_query(
            """
            SELECT i.*, u.username as owner_name, t.name as type_name
            FROM items i
            JOIN users u ON i.owner_id = u.id
            JOIN item_types t ON i.type_id = t.id
            ORDER BY i.created_at DESC
            """,
            fetch=True
        )
        for item in items:
            if isinstance(item['custom_values'], str):
                item['custom_values'] = json.loads(item['custom_values'])
            elif item['custom_values'] is None:
                item['custom_values'] = {}
        return items

    def search_items(self, type_id: int, keyword: str) -> list:
        """Search items by type and keyword."""
        keyword_pattern = f"%{keyword}%"
        items = db.execute_query(
            """
            SELECT i.*, u.username as owner_name, t.name as type_name
            FROM items i
            JOIN users u ON i.owner_id = u.id
            JOIN item_types t ON i.type_id = t.id
            WHERE i.type_id = ? AND (i.name LIKE ? OR i.description LIKE ?)
            ORDER BY i.created_at DESC
            """,
            (type_id, keyword_pattern, keyword_pattern),
            fetch=True
        )
        for item in items:
            if isinstance(item['custom_values'], str):
                item['custom_values'] = json.loads(item['custom_values'])
            elif item['custom_values'] is None:
                item['custom_values'] = {}
        return items

    def delete_item(self, item_id: int, owner_id: int = None) -> bool:
        """Delete an item."""
        if owner_id:
            db.execute_query(
                "DELETE FROM items WHERE id = ? AND owner_id = ?",
                (item_id, owner_id)
            )
        else:
            db.execute_query(
                "DELETE FROM items WHERE id = ?",
                (item_id,)
            )
        return True

    def get_item_by_id(self, item_id: int) -> dict:
        """Get a single item by ID."""
        item = db.execute_query(
            """
            SELECT i.*, u.username as owner_name, t.name as type_name
            FROM items i
            JOIN users u ON i.owner_id = u.id
            JOIN item_types t ON i.type_id = t.id
            WHERE i.id = ?
            """,
            (item_id,),
            fetchone=True
        )
        if item:
            if isinstance(item['custom_values'], str):
                item['custom_values'] = json.loads(item['custom_values'])
            elif item['custom_values'] is None:
                item['custom_values'] = {}
        return item
