import sqlite3
import os
from datetime import datetime

DB_PATH = "users.db"

def init_db():
    """
    Initialize database with users and referrals tables.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TEXT,
            referred_by INTEGER,
            referral_count INTEGER DEFAULT 0,
            credits INTEGER DEFAULT 0
        )
    ''')
    
    # Referrals tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER,
            referred_id INTEGER,
            created_at TEXT,
            FOREIGN KEY (referrer_id) REFERENCES users(user_id),
            FOREIGN KEY (referred_id) REFERENCES users(user_id)
        )
    ''')
    
    # History tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mode TEXT,
            content_preview TEXT,
            result_preview TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user(user_id):
    """Get user by ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(user_id, username, first_name, referred_by=None):
    """Create new user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if user exists
    existing = get_user(user_id)
    if existing:
        conn.close()
        return False
    
    cursor.execute('''
        INSERT INTO users (user_id, username, first_name, joined_at, referred_by, referral_count, credits)
        VALUES (?, ?, ?, ?, ?, 0, 0)
    ''', (user_id, username, first_name, datetime.now().isoformat(), referred_by))
    
    # If referred by someone, add referral
    if referred_by:
        cursor.execute('''
            INSERT INTO referrals (referrer_id, referred_id, created_at)
            VALUES (?, ?, ?)
        ''', (referred_by, user_id, datetime.now().isoformat()))
        
        # Increment referrer's count
        cursor.execute('''
            UPDATE users SET referral_count = referral_count + 1
            WHERE user_id = ?
        ''', (referred_by,))
        
        # Check if referrer reached milestone (3 refs)
        cursor.execute("SELECT referral_count FROM users WHERE user_id = ?", (referred_by,))
        count = cursor.fetchone()[0]
        
        if count % 3 == 0:  # Every 3 referrals
            cursor.execute('''
                UPDATE users SET credits = credits + 1
                WHERE user_id = ?
            ''', (referred_by,))
    
    conn.commit()
    conn.close()
    return True

def get_referral_stats(user_id):
    """Get user's referral stats."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT referral_count, credits FROM users WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"referrals": result[0], "credits": result[1]}
    return {"referrals": 0, "credits": 0}

def use_credit(user_id):
    """Use one credit for premium analysis."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET credits = credits - 1
        WHERE user_id = ? AND credits > 0
    ''', (user_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def add_to_history(user_id, mode, content_preview, result_preview):
    """Add analysis to user's history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO history (user_id, mode, content_preview, result_preview, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, mode, content_preview[:200], result_preview[:500], datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_user_history(user_id, limit=5):
    """Get user's recent analyses."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT mode, content_preview, result_preview, created_at 
        FROM history 
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (user_id, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    history = []
    for row in results:
        history.append({
            "mode": row[0],
            "content": row[1],
            "result": row[2],
            "date": row[3]
        })
    
    return history

# Initialize on import
init_db()
