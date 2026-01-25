import librosa
from audio import AudioSignal
from config import SR

class AudioLoader:
    """
    Responsible for loading an audio file from disk and return an AudioSignal object for the audio

    It enforces 
     - target sampling rate
     - mono audio
    """

    def __init__(self, target_sr:int = SR):

        if target_sr <= 0:
            raise ValueError("target_sr must be positive")
        self._target_sr = target_sr

    def load(self, path: str) -> AudioSignal:
        """Loads a audio file from it's path and returns AudioSignal object"""
        try:
            y, sr = librosa.load(path, sr=self._target_sr, mono=True)
        except FileNotFoundError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to load audio file: {path}") from e

        return AudioSignal(y, sr)