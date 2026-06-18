import sqlite3
import string
import random
from datetime import datetime

DB_FILE = "recency_tracker.db"

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        po_name TEXT NOT NULL,
        round_name TEXT NOT NULL,
        room_number TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )''')
    
    # Players table
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        name TEXT NOT NULL,
        list_index INTEGER DEFAULT 0,
        position_in_list INTEGER DEFAULT 0,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    )''')
    
    conn.commit()
    conn.close()

def generate_session_code(length=4):
    """Generate a random session code (uppercase letters + digits)."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_session(po_name, round_name, room_number):
    """Create a new session and return session ID and code."""
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    code = generate_session_code()
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    try:
        c.execute('''INSERT INTO sessions (id, po_name, round_name, room_number, code)
                     VALUES (?, ?, ?, ?, ?)''',
                  (session_id, po_name, round_name, room_number, code))
        conn.commit()
        return session_id, code
    except sqlite3.IntegrityError:
        conn.close()
        return None, None
    finally:
        conn.close()

def get_session_by_code(code):
    """Get session details by code."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, po_name, round_name, room_number FROM sessions WHERE code = ? AND is_active = 1', (code,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {'id': result[0], 'po_name': result[1], 'round_name': result[2], 'room_number': result[3]}
    return None

def get_session_by_id(session_id):
    """Get session details by ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, po_name, round_name, room_number, code FROM sessions WHERE id = ?', (session_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {'id': result[0], 'po_name': result[1], 'round_name': result[2], 'room_number': result[3], 'code': result[4]}
    return None

def add_player(session_id, name):
    """Add a player to a session."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO players (session_id, name) VALUES (?, ?)',
              (session_id, name))
    conn.commit()
    conn.close()

def get_players(session_id):
    """Get all players in a session, organized by list."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT id, name, list_index, position_in_list FROM players 
                 WHERE session_id = ? 
                 ORDER BY list_index, position_in_list''', (session_id,))
    results = c.fetchall()
    conn.close()
    
    # Organize into lists
    lists = {}
    for player_id, name, list_idx, pos in results:
        if list_idx not in lists:
            lists[list_idx] = []
        lists[list_idx].append({'id': player_id, 'name': name, 'position': pos})
    
    return lists

def move_player(session_id, player_id):
    """Move a player to the next list."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Get current list and position
    c.execute('SELECT list_index FROM players WHERE id = ?', (player_id,))
    result = c.fetchone()
    
    if result:
        current_list = result[0]
        c.execute('UPDATE players SET list_index = ? WHERE id = ?',
                  (current_list + 1, player_id))
        conn.commit()
    
    conn.close()
