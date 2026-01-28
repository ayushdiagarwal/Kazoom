import sqlite3
from main import main
from config import DB_SONG_META

def index_all():
    conn = sqlite3.connect(DB_SONG_META)
    cursor = conn.cursor()

    cursor.execute("SELECT song_id, path FROM songs ORDER BY song_id")
    rows = cursor.fetchall()

    if not rows:
        print("No songs found in metadata database.")
        return

    print(f"Found {len(rows)} songs. Starting indexing...\n")
    i = 0
    for song_id, path in rows:
        i += 1
        if i <= 24:
            print(f"{i}: skip ...")
            continue
        print(f"[INDEXING] song_id={song_id}")
        print(f"           path={path}")

        try:
            main(path, "I", song_id)
        except Exception as e:
            print(f"[ERROR] Failed to index song_id={song_id}")
            print(e)
            print("Continuing...\n")
            continue

        print(f"[DONE] song_id={song_id}\n")
        

    conn.close()
    print("Indexing complete.")

if __name__ == "__main__":
    index_all()