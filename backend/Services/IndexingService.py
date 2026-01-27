from Audio.loader import AudioLoader
from Pipeline.fingerprint import FingerprintPipeline
from Database.base import FingerprintStore

"""
Dependencies are injected rather than created here so configuration and
implementation choices are centralized and the service remains reusable,
testable, and free of hard-coded policies.
"""

class IndexingService:
    "Responsible for indexing known audio files into the fingerprint Store"

    def __init__(self,
        loader: AudioLoader,
        pipeline: FingerprintPipeline,
        store: FingerprintStore
        ):
        self._loader = loader
        self._pipeline = pipeline
        self._store = store

    def index(self, path: str, song_id:int) -> None:
        "Index a single audio file under a given song_id"

        audio = self._loader.load(path)
        fingerprints = self._pipeline.convert(audio, song_id)

        for fp in fingerprints:
            self._store.insert(fp)