# -*- coding: utf-8 -*-
# model/user_manager.py
"""
User Management: Registration, Login, Approval.
"""
import bcrypt
from model.database import db

class UserManager:
    """Handles user-related database operations."""

    def register(self, username: str, password: str, email: str, phone: str, address: str) -> dict:
        """Register a new user with 'pending' status."""
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        try:
            user_id = db.execute_query(
                """
                INSERT INTO users (username, password_hash, email, phone, address, role)
                VALUES (?, ?, ?, ?, ?, 'pending')
                """,
                (username, password_hash, email, phone, address)
            )
            return {'id': user_id, 'username': username, 'role': 'pending'}
        except Exception as e:
            if 'UNIQUE constraint' in str(e):
                return None
            raise

    def login(self, username: str, password: str) -> dict:
        """Authenticate user."""
        user = db.execute_query(
            "SELECT * FROM users WHERE username = ?",
            (username,),
            fetchone=True
        )
        
        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            del user['password_hash']
            return user
        return None

    def get_pending_users(self) -> list:
        """Get all users with 'pending' status."""
        return db.execute_query(
            "SELECT id, username, email, phone, address, created_at FROM users WHERE role = 'pending'",
            fetch=True
        )

    def approve_user(self, user_id: int) -> bool:
        """Approve a pending user."""
        db.execute_query(
            "UPDATE users SET role = 'user' WHERE id = ? AND role = 'pending'",
            (user_id,)
        )
        return True

    def reject_user(self, user_id: int) -> bool:
        """Reject a pending user."""
        db.execute_query(
            "DELETE FROM users WHERE id = ? AND role = 'pending'",
            (user_id,)
        )
        return True

    def get_user_by_id(self, user_id: int) -> dict:
        """Get user by ID."""
        user = db.execute_query(
            "SELECT id, username, email, phone, address, role, created_at FROM users WHERE id = ?",
            (user_id,),
            fetchone=True
        )
        return user
