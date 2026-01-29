from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] 

SR = 44100
FRAME_SIZE = 1024
N_FFT = 2048
HOP_SIZE = 512

DB_DIR = f"{BASE_DIR}/db"
DB_FILENAME = f"{DB_DIR}/fingerprints.pkl"
DB_SONG_META = f"{DB_DIR}/songs_metadata.db"
DB_PATH = f"{DB_DIR}/fingerprints.db"
DB_SQL = f"{DB_DIR}/export.sql"

MIN_TIME_DELTA = 0.5
MAX_TIME_DELTA = 1.2

FAN_OUT = 10 
NEIGHBORHOOD_SIZE = 25
THRESHOLD_MIN_DB = -40