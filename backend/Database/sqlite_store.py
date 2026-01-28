import sqlite3
from Fingerprint.fingerprint import Fingerprint
from Database.base import FingerprintStore

class SQLiteFingerprintStore(FingerprintStore):

    """
    SQLite-backed fingerprint store
    """

    def __init__(self, db_path:str):
        self._conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fingerprints (
                hash INTEGER NOT NULL,
                song_id INTEGER NOT NULL,
                anchor_time REAL NOT NULL 
                )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hash ON fingerprints(hash)
        """)

        self._conn.commit()

    def insert(self, fingerprint: Fingerprint) -> None:
        """Insert a fingerprint into the sqlite3 db"""

        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO fingerprints (hash, song_id, anchor_time) VALUES (?, ?, ?)",
            (fingerprint.hash_val, fingerprint.song_id, fingerprint.anchor_time)
        )
        self._conn.commit()

    def lookup(self, hash_val:int) -> list[Fingerprint]:
        """lookup a hash_val in the sqlite3 db to return a list of corresponding fingerprints"""
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT hash, song_id, anchor_time FROM fingerprints WHERE hash = ?",
            (hash_val,)
        )

        rows = cursor.fetchall()
        return [
            Fingerprint(hash_val=row[0], song_id=row[1], anchor_time=row[2])
            for row in rows
        ]
    
    def close(self):
        self._conn.close()