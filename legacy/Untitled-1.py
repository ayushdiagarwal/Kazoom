# %%
import numpy as np
import matplotlib.pyplot as plt
import librosa

# %%
# CONSTANTS

#SONG_ID = 8
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
        freq = f * SR / FRAME_SIZE
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
import hashlib

# These constants define the bit allocation for packing the hash
FREQ_BITS = 10 
TIME_BITS = 8
HASH_BITS = FREQ_BITS * 2 + TIME_BITS  # Total bits for the hash

# Hashing function using a more robust bit packing method
def encode_hash(f1, f2, delta_t):
    """
    Encodes two frequencies and their time difference into a single hash.
    Uses bit manipulation to pack the information efficiently.
    """
    # Use hashlib for a more robust initial hash
    # This combines the three values into a single hashable string
    key = f"{int(f1)}-{int(f2)}-{int(delta_t)}".encode('utf-8')
    
    # Use SHA-1, then take a portion of its output for our fingerprint
    # This creates a highly unique integer from the key
    h = hashlib.sha1(key)
    
    # Take the first few bytes and convert to an integer
    # We use HASH_BITS to ensure the hash fits within our defined size
    return int(h.hexdigest()[:HASH_BITS // 4], 16)


def create_hashes(peaks, song_id):
    """
    Generates a dictionary of hashes from a list of spectral peaks.
    A hash is created from a pair of peaks (an anchor and a target).
    
    Returns:
        A dictionary where keys are the hashes and values are lists of 
        tuples: (song_id, anchor_peak_time).
    """
    hashes = {}
    
    # These parameters define the "target zone" for pairing peaks
    MIN_TIME_DELTA = 0.5  # Minimum time offset in seconds
    MAX_TIME_DELTA = 2.0  # Maximum time offset in seconds
    FAN_OUT = 15          # Max number of peaks to pair with an anchor

    total_peaks = len(peaks)
    for i in range(total_peaks):
        f1, t1 = peaks[i]
        
        pairs_formed = 0
        for j in range(i + 1, total_peaks):
            f2, t2 = peaks[j]
            delta_t = t2 - t1

            # Check if the time difference is within our target window
            if MIN_TIME_DELTA <= delta_t <= MAX_TIME_DELTA:
                # Create a hash from the frequencies and time delta
                hash_val = encode_hash(f1, f2, delta_t)

                # Store the hash with the song_id and the ANCHOR's absolute time
                if hash_val not in hashes:
                    hashes[hash_val] = []
                hashes[hash_val].append((song_id, t1))
                
                pairs_formed += 1
                if pairs_formed >= FAN_OUT:
                    break
            
            # Optimization: If we've passed the max time delta, move to the next anchor
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
import collections
import pickle

def load_hashes():
    """Loads the fingerprint database from a pickle file."""
    with open('fingerprints.pkl', 'rb') as f:
        return pickle.load(f)

# 'hashes' is the variable you generated from fingerprinting your query song.
# Its structure is {hash: [(song_id, time), ...]}
# Example: {4723200: [(4, np.float64(2.5))]}

def match_hashes(hashes):
    # 1. Load the database of saved song fingerprints
    saved_hashes = load_hashes()

    # 2. Run the matching algorithm directly on the query's hashes
    histogram = collections.defaultdict(int)
    for qhash, t_q_frames in hashes.items():
        if qhash in saved_hashes:
            for db_song_id, t_db_frames in saved_hashes[qhash]:
                offset_frames = int(t_db_frames - t_q_frames)
                key = (int(db_song_id), offset_frames)
                histogram[key] += 1


    # 3. Find the song with the most matching offsets
    if not histogram:
        print("No matches found.")
    else:
        # Find the (song_id, offset) pair with the highest vote count
        best_match = max(histogram.items(), key=lambda item: item[1])
        
        (song_id, offset), num_votes = best_match

        print("--- Match Found! ---")
        print(f"Best Match: Song ID {song_id}")
        print(f"Confidence (votes): {num_votes}")

        # Optional: You can add your debugging block here if needed
        print("\n--- Debug Info ---")
        query_hashes_set = set(hashes.keys())
        db_hashes_set = set(saved_hashes.keys())
        common_hashes = query_hashes_set.intersection(db_hashes_set)
        print(f"Total Hashes in Query: {len(query_hashes_set)}")
        print(f"Total Hashes in Database: {len(db_hashes_set)}")
        print(f"Number of Common Hashes Found: {len(common_hashes)}")

# %%
# for query
#match_hashes(hashes)

def find_match(SONG_LOCATION, SONG_ID):
    peaks = load_song(SONG_LOCATION)
    hashes = create_hashes(peaks, SONG_ID)

    match_hashes(hashes)

# find_match("query/countryroads.mp3", 6)


# %%
import librosa
import numpy as np
import pickle
import collections
from scipy.ndimage import maximum_filter
from scipy.ndimage import generate_binary_structure

def save_db():
    """Builds and saves the fingerprint database."""
    songs = [
        ("songs/Hangman.mp3", 0),
        ("songs/The Moon.mp3", 1),
        ("songs/02. Eleanor Rigby.mp3", 2),
        ("songs/03. I'm Only Sleeping.mp3",3)
    ]
    
    db = collections.defaultdict(list)
    for location, song_id in songs:
        print(f"Fingerprinting '{location}' with SONG_ID = {song_id}")
        peaks = load_song(location)
        print(peaks[:5])
        hashes = create_hashes(peaks, song_id)
        for hash_val, hash_info in hashes.items():
            db[hash_val].extend(hash_info)
            
    with open('fingerprints.pkl', 'wb') as f:
        pickle.dump(db, f)
    print("Database saved successfully.")

def fingerprint_query(song_location):
    peaks = load_song(song_location)
    hashes_with_id = create_hashes(peaks, song_id=-1)
    query_hashes = {}
    for h, lst in hashes_with_id.items():
        if lst:
            query_hashes[h] = lst[0][1]
    return query_hashes

# THE CORRECTED MATCHING FUNCTION
def find_match(song_location):
    """Finds the best match for a query song against the database."""
    
    # 1. Load the database
    with open('fingerprints.pkl', 'rb') as f:
        saved_hashes = pickle.load(f)
        
    # 2. Fingerprint the query song (without assigning a real ID)
    query_hashes = fingerprint_query(song_location)
    
    # 3. Run the matching algorithm
    histogram = collections.defaultdict(int)
    for qhash, t_q_frame in query_hashes.items():
        if qhash in saved_hashes:
            for db_song_id, t_db_frame in saved_hashes[qhash]:
                offset_frames = int(t_db_frame - t_q_frame)
                histogram[(int(db_song_id), offset_frames)] += 1
                
    # 4. Find the winning song
    if not histogram:
        print("No matches found.")
        return None
    
    song_votes = collections.defaultdict(int)
    for (song_id, offset), votes in histogram.items():
        song_votes[song_id] += votes

    if not song_votes:
        print("No matches found.")
        return None

    sorted_songs = sorted(song_votes.items(), key=lambda item: item[1], reverse=True)

    best_song_id, best_song_votes = sorted_songs[0]

    if len(sorted_songs) > 1:
        second_best_votes = sorted_songs[1][1]
        confidence = (1 - (second_best_votes / best_song_votes)) * 100
        print(f"Confidence: {confidence:.2f}% (Winner has {best_song_votes} votes, runner-up has {second_best_votes} votes)")
        print(f"Best song: Song ID {best_song_id}")
    else:
        confidence = 100.0
        print(f"Confidence: 100% (Only one song found with {best_song_votes} votes)")

    # You can now set a threshold on this confidence percentage
    if confidence < 75: # Example threshold
        print("Match found, but confidence is too low.")
        return None

    # Continue with reporting the best_match from the original histogram
    print(f"Best Match: Song ID {best_song_id}")

# %%
save_db()

# %%
find_match("query/hangman.mp3")

# %%
find_match("query/rigby.mp3")

# %%
import pickle
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

counts = count_song_ids("fingerprints.pkl", song_ids=(0,1,2))
print(counts)



# %%
find_match("query/hangman.mp3")

# %%
find_match("query/moon.mp3")

# %%
find_match("query/hangman.mp3")

# %%
find_match("query/rigby.mp3")

# %%
find_match("query/sleeping.mp3")

# %%



