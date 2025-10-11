# %%
import numpy as np
import matplotlib.pyplot as plt
import librosa

# %%
# CONSTANTS

SR = 44100
FRAME_SIZE = 1024
HOP_SIZE = 512

SONG_LOCATION = "query/countryroads.mp3"

# %%

def load_song(song_location):
    y, sr = librosa.load(song_location, sr=SR)  

    print(f"Shape: {y.shape}, Sample Rate: {SR}")

    time = np.linspace(0, len(y)/sr, len(y)) # start, stop, no of points
    # plt.figure(figsize=(12, 4))
    # plt.plot(time, y, color='blue')
    # plt.show()

    return spectro(y)

# %%
def spectro(y):
    D = librosa.stft(y, n_fft = 2048, hop_length=HOP_SIZE)

    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    # plt.figure(figsize=(12, 6))
    # librosa.display.specshow(S_db, sr=SR, hop_length=512,
    #                         x_axis='time', y_axis='hz', cmap='magma')
    # plt.colorbar(format="%+2.0f dB")
    # plt.title("Spectrogram (dB)")
    # plt.show()

    return find_peaks(S_db, y)

# %%
from scipy.ndimage import maximum_filter, generate_binary_structure, iterate_structure

def find_peaks(spec_db, y):

    from scipy.ndimage import maximum_filter
    neighborhood_size = (25, 25)
    local_max = maximum_filter(spec_db, size=neighborhood_size) == spec_db
    peaks = np.argwhere(local_max)

    # filtering out the low frequencies
    peaks = [(t, f) for f, t in peaks if spec_db[f, t] > -40]  # -40 dB threshold

    peak_points = []
    for (t, f) in peaks:
        time = t * HOP_SIZE / SR
        freq = f * SR / 2048  # changed this from FRAME_SIZE -> n_fft
        peak_points.append((freq, time))

    #plot_peaks(y,spec_db, peak_points)    

    return peak_points



# %%
    
def plot_peaks(y, spec_db, peak_points):    
    # plot peaks
    plt.figure(figsize=(12, 6))

    # Plot spectrogram
    plt.imshow(spec_db, origin="lower", aspect="auto", cmap="magma",
            extent=[0, len(y)/SR, 0, SR/2])

    # Overlay peaks
    freqs = [p[0] for p in peak_points]
    times = [p[1] for p in peak_points]
    plt.scatter(times, freqs, color="cyan", marker=".", s=10, label="Peaks")

    plt.colorbar(label="Magnitude (dB)")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Spectrogram with Detected Peaks")
    plt.legend(loc="upper right")
    plt.show()

# %%
def encodehash(f_a, f_b, delta_t_frames):
    # f_a, f_b: frequency bin indices (int)
    # delta_t_frames: integer difference in frames (anchor->target)
    f_a = int(f_a) & ((1 << 11) - 1)
    f_b = int(f_b) & ((1 << 11) - 1)
    dt  = int(delta_t_frames) & ((1 << 10) - 1)

    hash_val = (f_a << (11 + 10)) | (f_b << 10) | dt
    return hash_val & 0xFFFFFFFF

def decodehash(hash_val):
    dt  = hash_val & ((1 << 10) - 1)
    f_b = (hash_val >> 10) & ((1 << 11) - 1)
    f_a = (hash_val >> (10 + 11)) & ((1 << 11) - 1)
    return f_a, f_b, dt


# %%
# These constants define the bit allocation for packing the hash
FREQ_BITS = 10 
TIME_BITS = 8
HASH_BITS = FREQ_BITS * 2 + TIME_BITS  # Total bits for the hash

def create_hashes(peaks, song_id):
    """
    Generates a dictionary of hashes from a list of spectral peaks.
    """
    # Sort peaks by time to ensure the process is deterministic
    peaks.sort(key=lambda x: x[1])
    
    hashes = {}
    
    MIN_TIME_DELTA = 0.5
    MAX_TIME_DELTA = 1.2  # Reduced to create more local fingerprints
    FAN_OUT = 10          # Reduced to limit hash collisions

    total_peaks = len(peaks)
    for i in range(total_peaks):
        f1, t1 = peaks[i]
        
        pairs_formed = 0
        for j in range(i + 1, total_peaks):
            f2, t2 = peaks[j]
            delta_t = t2 - t1

            if MIN_TIME_DELTA <= delta_t <= MAX_TIME_DELTA:
                hash_val = encodehash(f1, f2, delta_t)

                if hash_val not in hashes:
                    hashes[hash_val] = []
                hashes[hash_val].append((song_id, t1))
                
                pairs_formed += 1
                if pairs_formed >= FAN_OUT:
                    break
            
            elif delta_t > MAX_TIME_DELTA:
                break
                
    return hashes

# %%
# Saving to local database using pickle for now
# We can move onto using a better database like redis later
import pickle
DB_FILENAME = "fingerprints.pkl"

def save_hashes(hashes):
    with open(DB_FILENAME, 'ab') as f:  
        pickle.dump(hashes, f)
    print(f"Successfully appended {len(hashes)} fingerprints to {DB_FILENAME}")

def load_hashes():
    with open(DB_FILENAME, 'rb') as f:
        loaded_hashes = pickle.load(f)
    
    return loaded_hashes

# %%
def load_hashes():
    """Loads the fingerprint database from a pickle file."""
    with open('fingerprints.pkl', 'rb') as f:
        return pickle.load(f)

# 'hashes' is the variable generated from fingerprinting your query song.
# Its structure is {hash: [(song_id, time), ...]}
# Example: {4723200: [(4, np.float64(2.5))]}


# %%
import collections
import os
import json 

def save_db():
    """Builds and saves the fingerprint database."""

    revolver_songs = sorted(os.listdir("./revolver/"))

    songs = [("./revolver/" + revolver_songs[i], i) for i in range(len(revolver_songs))]
    
    db = collections.defaultdict(list)
    song_info_map = {}

    for location, song_id in songs:
        print(f"Fingerprinting '{location}' with SONG_ID = {song_id}")

        base_name = os.path.basename(location)
        song_name, _ = os.path.splitext(base_name)
        song_info_map[song_id] = song_name

        peaks = load_song(location)
        print(peaks[:5])
        hashes = create_hashes(peaks, song_id)
        for hash_val, hash_info in hashes.items():
            db[hash_val].extend(hash_info)
            
    with open('fingerprints.pkl', 'wb') as f:
        pickle.dump(db, f)
    print("Database saved successfully.")
    
    with open('song_info.json', 'w') as f:
        json.dump(song_info_map, f, indent=4)
    print("Song information map saved successfully to song_info.json")

def fingerprint_query(song_location):
    peaks = load_song(song_location)
    hashes_with_id = create_hashes(peaks, song_id=-1)
    query_hashes = {}
    for h, lst in hashes_with_id.items():
        if lst:
            query_hashes[h] = lst[0][1]
    return query_hashes

def find_match(song_location):
    """
    Finds the best match for a query song using robust peak alignment logic.
    """
    with open('fingerprints.pkl', 'rb') as f:
        saved_hashes = pickle.load(f)
        
    query_hashes = fingerprint_query(song_location)
    
    histogram = collections.defaultdict(int)
    for qhash, t_q_frame in query_hashes.items():
        if qhash in saved_hashes:
            for db_song_id, t_db_frame in saved_hashes[qhash]:
                offset = int(t_db_frame - t_q_frame)
                histogram[(int(db_song_id), offset)] += 1
                
    if not histogram:
        print("No matches found.")
        return None
    
    # Find the peak alignment for each song 
    song_peaks = collections.defaultdict(int)
    for (song_id, offset), votes in histogram.items():
        if votes > song_peaks[song_id]:
            song_peaks[song_id] = votes

    if not song_peaks:
        print("No matching alignments found.")
        return None

    # Sort songs by the strength of their best alignment
    sorted_songs = sorted(song_peaks.items(), key=lambda item: item[1], reverse=True)
    
    best_song_id, best_song_votes = sorted_songs[0]

    # Calculate and print confidence based on peak alignments
    if len(sorted_songs) > 1:
        second_best_votes = sorted_songs[1][1]
        confidence = (1 - (second_best_votes / best_song_votes)) * 100
        print(f"Confidence: {confidence:.2f}%")
        print(f"Best Match: Song ID {best_song_id}")
        print(f"(Winner's best alignment: {best_song_votes} votes, Runner-up's best alignment: {second_best_votes} votes)")
    else:
        confidence = 100.0
        print(f"Confidence: 100%")
        print(f"Best Match: Song ID {best_song_id} (Only one song found with {best_song_votes} votes)")

    # We can still use a threshold on this more reliable confidence score
    if confidence < 30: # A lower threshold might be suitable now
        print("\nMatch found, but confidence is too low to be certain.")
        return None

    return best_song_id

# %%
#save_db()

# %%
from collections import Counter

def count_song_ids(pkl_path, song_ids=(0,1,2)):
    with open(pkl_path, "rb") as f:
        saved_hashes = pickle.load(f)

    counter = Counter()
    for hash_val, entries in saved_hashes.items():
        for song_id, t in entries:
            if song_id in song_ids:
                counter[song_id] += 1

    # return results in consistent order
    return {sid: counter.get(sid, 0) for sid in song_ids}

# counts = count_song_ids("fingerprints.pkl", song_ids=(0,1,2))
# print(counts)

# %%
import sounddevice as sd
from scipy.io.wavfile import write
import os
import time

SR = 44100      # Sample Rate
DURATION = 15   # seconds to record
TEMP_FILENAME = "temp_query.wav"

def song_from_id(id):
    with open('song_info.json', 'r') as f:
            song_info_map = json.load(f)
            
            if id is not None:
                song_name = song_info_map.get(str(id), "Unknown Song")
                print(f"\nMatch Found!\n\n")
                print(f"==> {song_name} <==")

def recognize_and_match():
    print("Get ready to play a song...")
    for t in range(3, 0, -1):
        print(t)
        time.sleep(1)

    print("\nRecording...")
    myrecording = sd.rec(int(DURATION * SR), samplerate=SR, channels=1)
    sd.wait()
    print("Recording finished.")
    write(TEMP_FILENAME, SR, myrecording)

    print("Analyzing...")
    try:
        with open('song_info.json', 'r') as f:
            song_info_map = json.load(f)

        best_song_id = find_match(TEMP_FILENAME) 

        if best_song_id is not None:
            song_name = song_info_map.get(str(best_song_id), "Unknown Song")
            print(f"\n--- Match Found! ---")
            print(f"==> {song_name} <==")

    finally:
        os.remove(TEMP_FILENAME)

# recognize_and_match()

# %%
song_from_id(find_match("query/sleeping.mp3"))

# %%



