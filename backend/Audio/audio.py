import numpy as np

class AudioSignal:

    def __init__(self, samples: np.ndarray, sample_rate: int):

        if not isinstance(samples, np.ndarray):
            raise TypeError("Samples must be a numpy array")
        
        if samples.ndim != 1:
            raise ValueError("AudioSignal expects a mono(1D) Signal")
        
        if sample_rate <= 0:
            raise ValueError("The sample rate of the audio signal must be positive")
        
        # discourages mutation as _ states an internal implementation detail
        self._samples = samples
        self._sample_rate = sample_rate

    # making properties read-only
    @property
    def samples(self) -> np.ndarray:
        """Returns raw audio samples"""
        return self._samples
    
    @property 
    def sample_rate(self) -> int:
        """Returns sample rate in Hz"""
        return self._sample_rate
    
    def num_samples(self) -> int:
        """Total number of samples"""
        return self._samples.shape[0]
    
    def duration(self) -> float:
        """Total duration of the audio in seconds"""
        return self.num_samples() / self._sample_rate
    
    def slice(self, start_time: float, end_time:float) -> "AudioSignal":
        """Returns new audio corresponding to time slice"""

        if start_time < 0 or end_time <= start_time:
            raise ValueError("Invalid slice times")
        
        start_idx = int(start_time * self._sample_rate)
        end_idx = int(end_time * self._sample_rate)
        end_idx = min(end_idx, self.num_samples())

        return AudioSignal(self._samples[start_idx:end_idx], self._sample_rate)
    
    def copy(self) -> "AudioSignal":
        """Return a deep copy of this AudioSignal."""
        return AudioSignal(self._samples.copy(), self._sample_rate)




