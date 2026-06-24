import sqlite3
from contextlib import contextmanager
from config import settings

DB_PATH = settings.DATABASE_URL.replace("sqlite:///", "")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vk_id INTEGER UNIQUE NOT NULL,
                name TEXT,
                gender TEXT,
                height REAL,
                weight REAL,
                experience TEXT,
                goal TEXT,
                place TEXT,
                split TEXT,
                timezone TEXT DEFAULT 'Europe/Moscow',
                reminder_time TEXT,
                registered INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS training_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                workout_name TEXT,
                FOREIGN KEY (user_id) REFERENCES users(vk_id)
            );
            CREATE INDEX IF NOT EXISTS idx_users_vk_id ON users(vk_id);
            CREATE INDEX IF NOT EXISTS idx_log_user_date ON training_log(user_id, date);
        """)
    migrate()
    clean_old_data()

def migrate():
    with get_db() as conn:
        cursor = conn.execute("PRAGMA user_version")
        version = cursor.fetchone()[0]
        if version < 1:
            try:
                conn.execute(
                    "ALTER TABLE users ADD COLUMN timezone TEXT DEFAULT 'Europe/Moscow'"
                )
            except sqlite3.OperationalError:
                pass
            conn.execute("PRAGMA user_version = 1")

def clean_old_data():
    """Удаляет эмодзи и другие лишние символы из полей, оставляя только ключевые слова."""
    with get_db() as conn:
        users = conn.execute("SELECT vk_id, gender, experience, goal, place, split FROM users").fetchall()
        for user in users:
            vk_id = user["vk_id"]
            clean_gender = clean_field(user["gender"], ["мужской", "женский"])
            clean_experience = clean_field(user["experience"], ["новичок", "средний", "опытный"])
            clean_goal = clean_field(user["goal"], ["похудение", "набор массы", "рельеф", "поддержка формы"])
            clean_place = clean_field(user["place"], ["зал", "дома"])
            clean_split = clean_field(user["split"], ["фулбоди", "верх/низ", "трёхдневный сплит"])

            conn.execute("""
                UPDATE users 
                SET gender=?, experience=?, goal=?, place=?, split=?
                WHERE vk_id=?
            """, (clean_gender, clean_experience, clean_goal, clean_place, clean_split, vk_id))

def clean_field(value, valid_options):
    """Оставляет только то допустимое значение, которое содержится в строке."""
    if not value:
        return value
    value_lower = value.lower()
    for option in valid_options:
        if option in value_lower:
            return option
    return value