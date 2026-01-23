## 1. What you’ve built (high-level architecture)

Right now your pipeline is:

```
Audio
 → STFT
 → Peak detection
 → Peak pairing (fan-out)
 → Hashing (f1, f2, Δt)
 → Inverted index: hash → [(song_id, time)]
 → Query hashes
 → Offset voting histogram
 → Best alignment wins
```

This is **correct in principle**. This is almost exactly how Shazam works.

So the advice below is about **engineering tradeoffs**, not correctness.

---

## 2. Core design problems (important)

### 🔴 Problem 1: Pickle as a database (this will hurt you)

Right now:

```python
saved_hashes = pickle.load(f)
```

This means:

- Entire DB loads into RAM
- No partial reads
- No concurrency
- No incremental updates
- Corruption risk

#### What breaks:

- > 1k songs → RAM + load time explode
- Multiple queries at once → impossible
- App crashes → DB might be gone

### ✅ Fix (incremental, realistic)

Use **one of these**, ordered by sanity:

#### Option A (best for now): SQLite

Schema:

```sql
CREATE TABLE fingerprints (
  hash INTEGER,
  song_id INTEGER,
  time REAL
);

CREATE INDEX idx_hash ON fingerprints(hash);
```

Why:

- Fast lookups
- On-disk
- Dead simple
- No infra

Lookup becomes:

```sql
SELECT song_id, time FROM fingerprints WHERE hash = ?
```

This is **exactly** what you want.

---

### 🔴 Problem 2: Hash entropy & collision behavior

Your hash:

```python
(f_a << ...) | (f_b << ...) | dt
```

Issues:

- `f_a` and `f_b` are **raw frequencies**, not quantized bins
- Floating → int conversion is lossy and inconsistent
- Δt is continuous seconds, then masked

#### What breaks:

- Slight pitch shifts
- Sample rate mismatch
- Recording noise
- Phone mic vs studio audio

### ✅ Fix: Quantize aggressively

Before hashing:

```python
freq_bin = int(freq / 20)        # 20–40 Hz buckets
time_bin = int(delta_t / 0.02)   # 20 ms resolution
```

Hash **bins**, not raw values.

Shazam uses _coarse_ hashes on purpose.

> Robust > precise

---

### 🔴 Problem 3: Peak explosion & noise sensitivity

This line:

```python
local_max = maximum_filter(spec_db, size=(25, 25)) == spec_db
```

You are:

- Finding **way too many peaks**
- Including harmonics + noise
- Doing O(N²) pairing afterward

#### What breaks:

- Longer songs
- Dense mixes
- High CPU

### ✅ Fix: Stronger peak filtering

Add **all three**:

1. **Top-K peaks per time slice**

```python
Keep top 5–10 peaks per frame
```

2. **Log-frequency axis**
   Use `librosa.cqt` or mel scale instead of linear FFT bins.

3. **Local thresholding**
   Instead of `> -40 dB`, use:

```python
spec_db > (local_mean + X dB)
```

This kills noise peaks hard.

---

## 3. Matching logic (this is good, but can be sharper)

### What you’re doing right

- Offset histogram ✔
- Song-specific peak alignment ✔
- Confidence via winner vs runner-up ✔

That’s the **right idea**.

### 🔴 Issue: Query hash subsampling

```python
query_hashes[h] = lst[0][1]
```

You’re:

- Throwing away multiple occurrences of same hash
- Losing temporal density info

### ✅ Fix: Keep all query times

Use:

```python
query_hashes[h].append(t_q)
```

Then vote on **all offsets**, not just first occurrence.

---

## 4. Recording & real-world robustness

### 🔴 Problem: 15s fixed recording

- Too long for UX
- Too noisy at start
- Silence pollutes hashes

### ✅ Fix:

- Start fingerprinting **after energy threshold**
- Stop early if confidence spikes

```python
If votes > threshold early → stop
```

---

## 5. System-level redesign (important)

If you were turning this into a _real app_, structure it like this:

### 📦 Offline indexing

```
indexer/
 ├─ audio_loader.py
 ├─ peak_detector.py
 ├─ hasher.py
 ├─ db_writer.py
```

Run once, produces DB.

---

### ⚡ Online query path

```
query/
 ├─ mic_capture.py
 ├─ fingerprint_query.py
 ├─ db_lookup.py
 ├─ matcher.py
```

No disk writes. No pickle. Stateless.

---

## 6. Performance scaling math (reality check)

Let’s be real:

- ~40 hashes/sec
- 10s clip → ~400 hashes
- Each hash returns maybe 5–50 DB entries

That’s:

```
400 × 20 = 8,000 offset votes
```

Totally fine.

With SQLite + index:

- Sub-100 ms lookup
- CPU bound, not IO bound

You’re safe up to **tens of thousands of songs**.

---

## 7. “If you want to go hard” upgrades

Optional, but serious:

### 🔥 Use MinHash / LSH

For coarse candidate pruning before offset voting.

### 🔥 GPU FFT batching

If you batch queries (not needed now).

### 🔥 Fingerprint compression

Store `(song_id, time)` packed into 64 bits.

---

## 8. Final blunt verdict

- ❌ Pickle DB will kill this project
- ❌ Hash precision is too fine
- ❌ Peak selection is too noisy
- ✅ Core algorithm is right
- ✅ Matching logic is solid
- ✅ This is _actually_ a legit systems project

If you want, next step I can:

- Redesign your **DB schema**
- Rewrite `find_match()` for SQLite
- Help you define **quantization constants**
- Or help you turn this into a clean CLI / backend service

Tell me which direction you want to push it.
