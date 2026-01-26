from Peak.peak import Peak
from Fingerprint.fingerprint import Fingerprint
from config import MIN_TIME_DELTA, MAX_TIME_DELTA, FAN_OUT
from Fingerprint.hasher import Hash
from Spectrogram.spectrogram import Spectrogram

class FingerprintGenerator:

    def __init__(self, min_time_delta:float=MIN_TIME_DELTA, max_time_delta:float=MAX_TIME_DELTA, fan_out:int = FAN_OUT):

        if min_time_delta < 0:
            raise ValueError("Min time delta needs to be positive")
        
        if max_time_delta < 0:
            raise ValueError("Max time delta needs to be positive")
        
        if fan_out < 0:
            raise ValueError("Fan out needs to be positive")

        self._min_time_delta = min_time_delta
        self._max_time_delta = max_time_delta
        self._fan_out = fan_out

    def create(self, peaks: list[Peak], spectrogram: Spectrogram,song_id = -1) -> list[Fingerprint]:
        
        """
        Generates a list of fingerprints from a list of spectral peaks
        """

        peaks.sort(key= lambda x: x.time)

        fingerprints = []

        total_peaks = len(peaks)

        for i in range(total_peaks):
            f1, t1 = peaks[i].freq, peaks[i].time

            pairs_formed = 0 

            for j in range(i+1, total_peaks):
                f2, t2 = peaks[j].freq, peaks[j].time
                delta_t = t2 - t1 


                delta_t_frames = round(delta_t * spectrogram.sr / spectrogram.hop_size)

                if self._min_time_delta <= delta_t <= self._max_time_delta:

                    f1_bin = round(f1 *  spectrogram.n_fft/ spectrogram.sr)

                    f2_bin = round(f2 *  spectrogram.n_fft/ spectrogram.sr)

                    hash_val = Hash.encode(f1_bin, f2_bin, delta_t_frames)

                    fingerprints.append(Fingerprint(hash_val, t1, song_id))

                    pairs_formed += 1 
                    if pairs_formed >= self._fan_out:
                        break

                elif delta_t > self._max_time_delta:
                    break

        return fingerprints