"""Database models and connection."""

import sqlite3
from datetime import datetime
from typing import Optional, List
from .config import DB_PATH


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            prompt TEXT NOT NULL,
            status TEXT DEFAULT 'processing',
            video_path TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()


# User operations
def create_user(username: str, password_hash: str) -> Optional[int]:
    """Create a new user."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_username(username: str) -> Optional[dict]:
    """Get user by username."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# Video operations
def create_video(video_id: str, user_id: int, prompt: str) -> int:
    """Create a new video record."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO videos (video_id, user_id, prompt, status, message) VALUES (?, ?, ?, ?, ?)",
        (video_id, user_id, prompt, "processing", prompt[:100])
    )
    conn.commit()
    video_db_id = cursor.lastrowid
    conn.close()
    return video_db_id


def update_video_status(video_id: str, status: str, video_path: str = None):
    """Update video status and path."""
    conn = get_db()
    cursor = conn.cursor()
    if video_path:
        cursor.execute(
            "UPDATE videos SET status = ?, video_path = ? WHERE video_id = ?",
            (status, video_path, video_id)
        )
    else:
        cursor.execute(
            "UPDATE videos SET status = ? WHERE video_id = ?",
            (status, video_id)
        )
    conn.commit()
    conn.close()


def get_user_videos(user_id: int) -> List[dict]:
    """Get all videos for a user."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM videos WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_video_by_id(video_id: str) -> Optional[dict]:
    """Get video by video_id."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos WHERE video_id = ?", (video_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_videos() -> List[dict]:
    """Get all videos."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# Initialize database on import
init_db()
