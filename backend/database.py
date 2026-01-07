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
            credits INTEGER DEFAULT 0,
            current_mode TEXT DEFAULT 'red_flag',
            last_active_at TEXT,
            streak_count INTEGER DEFAULT 0
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

    # --- AUTO MIGRATION (Ensuring columns exist) ---
    columns_to_add = [
        ("current_mode", "TEXT DEFAULT 'red_flag'"),
        ("last_active_at", "TEXT"),
        ("streak_count", "INTEGER DEFAULT 0"),
        ("joined_at", "TEXT"),
        ("referred_by", "INTEGER"),
        ("referral_count", "INTEGER DEFAULT 0"),
        ("credits", "INTEGER DEFAULT 0")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass # Column already exists
    
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

def get_user_mode(user_id):
    """Get user's current mode."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT current_mode FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "red_flag"

def set_user_mode(user_id, mode):
    """Set user's current mode."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET current_mode = ?
        WHERE user_id = ?
    ''', (mode, user_id))
    conn.commit()
    conn.close()

from datetime import datetime, timedelta

def update_streak(user_id):
    """Update user streak and return (count, reward_given)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT last_active_at, streak_count, credits FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return 0, False
        
    last_active, count, credits = result
    today = datetime.now().date()
    
    reward_given = False
    new_count = count
    
    if last_active:
        last_date = datetime.strptime(last_active, '%Y-%m-%d').date()
        if last_date == today:
            # Already checked today
            conn.close()
            return count, False
        elif last_date == today - timedelta(days=1):
            # Continued streak
            new_count += 1
            if new_count % 7 == 0:
                # Reward every 7 days
                cursor.execute("UPDATE users SET credits = credits + 1 WHERE user_id = ?", (user_id,))
                reward_given = True
        else:
            # Streak broken
            new_count = 1
    else:
        # First time
        new_count = 1
        
    cursor.execute('''
        UPDATE users 
        SET last_active_at = ?, streak_count = ?
        WHERE user_id = ?
    ''', (today.strftime('%Y-%m-%d'), new_count, user_id))
    
    conn.commit()
    conn.close()
    return new_count, reward_given

# Initialize on import
init_db()
