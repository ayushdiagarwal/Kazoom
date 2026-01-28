import sqlite3
from pathlib import Path
from config import DB_SONG_META

# Creating database for the song metadata

SQL_FILE = "export.sql"     
DB_FILE = DB_SONG_META   

sql_script = Path(SQL_FILE).read_text(encoding="utf-8")

conn = sqlite3.connect(DB_FILE)

try:
    conn.executescript(sql_script)
    conn.commit()
    print(f"Database created: {DB_FILE}")
except sqlite3.Error as e:
    print("SQLite error:", e)
finally:
    conn.close()
