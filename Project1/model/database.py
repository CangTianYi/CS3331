# -*- coding: utf-8 -*-
# model/database.py
"""
SQLite Database Manager for local storage.
"""
import os
import sqlite3

# Path to SQLite database
SQLITE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'campus_xianyu.db')

class Database:
    """Singleton database connection manager using SQLite."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize SQLite database."""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
        self._create_tables()

    def _create_tables(self):
        """Create all required tables."""
        conn = sqlite3.connect(SQLITE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                role TEXT DEFAULT 'pending' CHECK(role IN ('admin', 'user', 'pending')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                custom_attributes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_id INTEGER NOT NULL,
                owner_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                location TEXT,
                contact_phone TEXT,
                contact_email TEXT,
                custom_values TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (type_id) REFERENCES item_types(id) ON DELETE CASCADE,
                FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Check if admin user exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admin_count = cursor.fetchone()[0]
        if admin_count == 0:
            import bcrypt
            default_password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
            cursor.execute(
                "INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
                ('admin', default_password, 'admin@campus.edu', 'admin')
            )
        
        conn.commit()
        conn.close()

    def get_connection(self):
        """Get a database connection."""
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def execute_query(self, query, params=None, fetch=False, fetchone=False):
        """Execute a query and optionally fetch results."""
        conn = self.get_connection()
        # Convert MySQL placeholders to SQLite
        query = query.replace('%s', '?')
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                result = [dict(row) for row in result]
            elif fetchone:
                result = cursor.fetchone()
                if result:
                    result = dict(result)
            else:
                conn.commit()
                result = cursor.lastrowid
            return result
        finally:
            cursor.close()
            conn.close()


# Global database instance
db = Database()
