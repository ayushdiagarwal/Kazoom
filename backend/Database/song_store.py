from config import DB_SONG_META
from Models.song import Song
import sqlite3

class SongStore:
    """
    Given a song_id, this will return the Song object
    """
    def get(self, song_id: int) -> Song: 
        if song_id < 0:
            raise ValueError("song_id can't be negative")
        
        conn = sqlite3.connect(DB_SONG_META)
        cursor = conn.cursor()

        cursor.execute("SELECT song_id, title, artist, album FROM songs WHERE song_id = ?;", (song_id,))

        row = cursor.fetchone()

        if len(row) == 0:
            raise LookupError("No such song_id present in the database")
        
        conn.close()

        song_id = row[0]
        song_name = row[1]
        song_artist = row[2]
        song_album = row[3]

        return Song(song_id,song_name,song_artist, song_album)