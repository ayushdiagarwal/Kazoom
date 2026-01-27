from Audio.loader import AudioLoader
from Pipeline.fingerprint import FingerprintPipeline
from Database.base import FingerprintStore
from Recognition.matcher import Matcher
from Recognition.result import Result

class RecognitionService:

    def __init__(self,
        loader: AudioLoader,
        pipeline: FingerprintPipeline,
        store: FingerprintStore,
        matcher: Matcher):
        
        self._loader = loader
        self._pipeline = pipeline
        self._store = store
        self._matcher = matcher

    def recognize(self, path: str) -> Result:
        # song_id will be unknown here (-1)

        song_id = -1
        audio = self._loader.load(path)
        fingerprints = self._pipeline.convert(audio, song_id)

        return self._matcher.match(self._store, fingerprints)



        



