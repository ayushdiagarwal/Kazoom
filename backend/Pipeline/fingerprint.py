from Audio.audio import AudioSignal
from Spectrogram.generator import SpectrogramGenerator
from Peak.detector import PeakDetector
from Fingerprint.fingerprint import Fingerprint
from Fingerprint.generator import FingerprintGenerator

"""
This pipeline converts an AudioSignal to a list of fingerprint
"""

class FingerprintPipeline:

    def __init__(self, spectrogram_generator: SpectrogramGenerator, peak_detector: PeakDetector, fingerprint_generator: FingerprintGenerator):
        """
        Dependencies are injected (not statically called) so the pipeline only
        orchestrates execution order and remains configurable, testable, and
        independent of specific DSP policies.
        """
        self._spectrogram_generator = spectrogram_generator
        self._peak_detector = peak_detector
        self._fingerprint_generator = fingerprint_generator

    def convert(self, audio:AudioSignal, song_id) -> list[Fingerprint]:
        
        spectrogram = self._spectrogram_generator.generate(audio)
        peaks = self._peak_detector.detect(spectrogram)
        fingerprints = self._fingerprint_generator.create(peaks, spectrogram, song_id)

        return fingerprints

