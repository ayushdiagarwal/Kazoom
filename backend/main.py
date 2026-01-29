from config import *
from Services.IndexingService import IndexingService
from Services.RecognitionService import RecognitionService
from Audio.loader import AudioLoader
from Pipeline.fingerprint import FingerprintPipeline
from Spectrogram.generator import SpectrogramGenerator
from Peak.detector import PeakDetector
from Fingerprint.generator import FingerprintGenerator
from Database.sqlite_store import SQLiteFingerprintStore
from Recognition.matcher import Matcher
from Recognition.result import Result
from Database.song_store import SongStore

def main(path, mode, song_id=-1):

	audio_loader = AudioLoader(SR)
	peak_detector = PeakDetector(NEIGHBORHOOD_SIZE, THRESHOLD_MIN_DB)
	fingerprint_store = SQLiteFingerprintStore(DB_PATH)

	spec_gen = SpectrogramGenerator(N_FFT, HOP_SIZE)
	fin_gen = FingerprintGenerator(MIN_TIME_DELTA, MAX_TIME_DELTA, FAN_OUT)

	fingerprint_pipeline = FingerprintPipeline(spec_gen, peak_detector, fin_gen)

	song_store = SongStore()

	if mode == "I":
		IndexingService(audio_loader, fingerprint_pipeline, fingerprint_store).index(path, song_id)
	elif mode == "R":
		matcher = Matcher()
		song:Result = RecognitionService(audio_loader, fingerprint_pipeline, fingerprint_store, matcher).recognize(path)

		if song.confidence < 30:
			print("No match found: Confidence less than 30%")
		else:
			print(song.song_id, song.confidence)
			return song_store.get(song.song_id), song.confidence
	else:
		raise ValueError("Invalid Mode of operation")
	
	return song_store.get(-1), 0
