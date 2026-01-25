from config import N_FFT, HOP_SIZE, SR
import numpy as np

class Spectrogram:
    """
    Spectrogram object always represents a log-magnitude spectrogram in db
    """
    
    def __init__(self, data_db: np.ndarray, sr: int = SR, hop_size:int = HOP_SIZE, n_fft: int = N_FFT):

        self._data_db = data_db

        if sr <= 0:
            raise ValueError("Sampling rate must be positive")

        if hop_size <= 0:
            raise ValueError("Hop size should be positive")
        
        if n_fft <= 0:
            raise ValueError("N-FFT should be positive")
        
        self._sr = sr
        self._hop_size = hop_size
        self._n_fft = n_fft

    @property
    def data_db(self):
        return self._data_db
    
    @property
    def sr(self):
        return self._sr
    
    @property
    def hop_size(self):
        return self._hop_size
    
    @property
    def n_fft(self):
        return self._n_fft

    