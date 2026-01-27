import librosa
import numpy as np 
from Audio.audio import AudioSignal
from Spectrogram.spectrogram import Spectrogram
from config import N_FFT, HOP_SIZE

class SpectrogramGenerator:

    def __init__(self, n_fft=N_FFT, hop_size=HOP_SIZE):

        self._n_fft = n_fft
        self._hop_size = hop_size
        

    def generate(self, audio: AudioSignal) -> Spectrogram:
        """
        Computes a dB-scaled spectrogram from an audio signal.

        Applies a short-time fourier transform (STFT) usig the configured FFT size and hop length, converts magnitude to decibels and returns a Spectrogram object.
        """
        
        stft = librosa.stft(audio.samples, n_fft = self._n_fft, hop_length = self._hop_size)

        data_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
        
        return Spectrogram(data_db, sr = audio.sample_rate, hop_size=self._hop_size, n_fft=self._n_fft)

