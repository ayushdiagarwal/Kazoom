from scipy.ndimage import maximum_filter
import numpy as np
from Spectrogram.spectrogram import Spectrogram
from Peak.peak import Peak

class PeakDetector:

    def __init__(self, neighbor_size:int = 25, min_db:float = -40.0):

        if neighbor_size <= 0:
            raise ValueError("Neighbor size needs to be positive")
        
        self._neighbor_size = neighbor_size
        self._min_db = min_db

    def detect(self, spectrogram: Spectrogram) -> list[Peak]:
        """
        Detects spectral peaks in a dB-scaled spectrogram

        A peak is defined as a local maxima within a square neighborhood and above a minimum amplitude threshold
        """
        
        neighborhood_size = (self._neighbor_size, self._neighbor_size)
        data_db = spectrogram.data_db

        local_max = maximum_filter(data_db, size = neighborhood_size) == data_db

        indices = np.argwhere(local_max)

        peak_points = []

        for f,t in indices:

            # skip if below minimum amplitude threshold

            if spectrogram.data_db[f,t] < self._min_db:
                continue

            time = t * spectrogram.hop_size/spectrogram.sr
            freq = f * spectrogram.sr/spectrogram.n_fft
            peak_points.append(Peak(freq, time))

        return peak_points