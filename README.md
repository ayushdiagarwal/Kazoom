# 🎵 Shazam Clone — Learning & Implementation Roadmap

This project is a self-learning journey to build a minimal Shazam-like app from scratch.  
The focus is on **understanding the algorithms**.

## What might be causing the issues

- Need to use a simpler algorithm to encode songs, SHA-1 Hashing is too harsh.
- Floating-Point Time Precision
  - (Floating-Point Time Precision: You store times as float64 and subtract them in match_hashes() (int(t_db_frames - t_q_frames)). These subtractions accumulate floating-point errors, causing the same peak pairs to hash to slightly different time deltas. Solution: Convert all times to integer frame indices immediately during fingerprinting and keep them as integers throughout.)
- Need to modify create_hashes function to form better packaging of peaks (must sort the peaks by their timestamp)

## 📚 Resources

- **Audio Processing Basics**: [Think DSP (free book)](https://greenteapress.com/wp/think-dsp/)
- **NumPy FFT Docs**: [numpy.fft](https://numpy.org/doc/stable/reference/routines.fft.html)
- **Librosa Docs**: [https://librosa.org/doc/latest/index.html](https://librosa.org/doc/latest/index.html)
- **Shazam Paper**: ["An Industrial-Strength Audio Search Algorithm" (Wang, 2003)](http://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf)

---

## 🚀 Roadmap / Checklist

### Phase 1: Foundations (Audio + FFT)

- [ ] Load a `.wav` file and plot its waveform
- [ ] Implement FFT on a short clip (0.5s)
- [ ] Plot frequency spectrum from FFT
- [ ] Test with a sine wave → FFT peak at correct frequency

📌 **Checkpoint 1:** Can I show a 440Hz sine wave has a peak near 440Hz?

---

### Phase 2: Time–Frequency Analysis (STFT / Spectrogram)

- [ ] Implement my own STFT (frames → FFT → stack)
- [ ] Plot spectrogram manually with `imshow`
- [ ] Compare with `librosa.stft` result

📌 **Checkpoint 2:** Can I explain the difference between FFT and STFT and generate both?

---

### Phase 3: Peak Picking

- [ ] Implement local maximum search in 2D spectrogram
- [ ] Add amplitude threshold to ignore weak peaks
- [ ] Plot constellation map (spectrogram + peaks)

📌 **Checkpoint 3:** Can I show only strong peaks in a noisy spectrogram?

---

### Phase 4: Fingerprinting

- [ ] For each peak, select nearby peaks → form pairs
- [ ] Create hash: `(f1, f2, Δt)`
- [ ] Store hashes with their time indices

📌 **Checkpoint 4:** Can I generate fingerprints for a 10-second clip?

---

### Phase 5: Database + Matching

- [ ] Build a small DB (dict or SQLite) to store fingerprints
- [ ] Add fingerprints for multiple songs
- [ ] Query with a test clip → match by overlapping hashes

📌 **Checkpoint 5:** Can I correctly identify a song from 3 candidates?

---

### Phase 6: Web App

- [ ] Build backend (Flask/FastAPI)
  - `/add_song` → process & store fingerprints
  - `/recognize` → upload clip & return match
- [ ] Add minimal frontend for recording/uploading audio

📌 **Checkpoint 6:** Can I record audio in browser and get a song match from my DB?

---

## 🎯 Final Goal

By the end, I’ll have a working Shazam-like demo that:

1. Learns fingerprints from audio files
2. Matches noisy clips against them
3. Runs end-to-end via a small web app

## Resources

### Peak finding

- https://www.audiolabs-erlangen.de/resources/MIR/FMP/C7/C7S1_AudioIdentification.html

Peaks in a spectrogram (local maxima) tend to be stable, even if there’s noise, MP3 compression, or background chatter.

A point (n0, k0) is a peak if its magnitude is greater than all neighbors within a rectangular neighborhood

∣X(n0​,k0​)∣≥∣X(n,k)∣∀(n,k)∈[n0​−τ:n0​+τ]×[k0​−κ:k0​+κ]
τ = how far you look in the time direction
κ = how far you look in the frequency direction

Bigger τ/κ = sparser constellation map (fewer peaks, only strong isolated ones)
After selecting peaks, you throw away magnitudes and keep only coordinates (time, frequency).
This looks like “stars in the night sky” → hence the name constellation map.

for i in range(rows):
for j in range(cols):
val = spec_db[i, j]
window = spec_db[i-τ:i+τ+1, j-κ:j+κ+1]
if val == np.max(window):
mark as peak
