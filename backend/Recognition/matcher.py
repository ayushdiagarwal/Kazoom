from Fingerprint.fingerprint import Fingerprint
from Database.base import FingerprintStore
from Recognition.result import Result
from collections import defaultdict

class Matcher:

    """
    Finds the best match for a query song using peak alignment logic 
    """

    def match(self, store:FingerprintStore, query_fingerprints: list[Fingerprint]) -> Result:
        
        histogram = defaultdict(int)

        # create histogram
        for q_fp in query_fingerprints:
            qhash = q_fp.hash_val
            q_t = q_fp.anchor_time

            candidates = store.lookup(qhash)

            for db_fp in candidates:
                db_song_id = db_fp.song_id
                t_db = db_fp.anchor_time

                offset = int(t_db - q_t)
                histogram[int(db_song_id), offset] += 1

        # No evidence
        if not histogram:
            return Result.no_match() # not found
        
        # For each song, find its strongest alignment
        song_peaks = defaultdict(int)
        
        for (song_id, _offset), votes in histogram.items():
            if votes > song_peaks[song_id]:
                song_peaks[song_id] = votes

        if not song_peaks:
            return Result.no_match()
        
        # sort songs by the strength of their best alignment 
        ranked_songs = sorted(song_peaks.items(), key = lambda item: item[1], reverse=True)
        best_song_id, best_song_votes = ranked_songs[0]

        if len(ranked_songs) == 1:
            confidence = 100.0
        else:
            second_best_votes = ranked_songs[1][1]
            confidence = (1 - (second_best_votes/best_song_votes)) * 100
        
        # here confidence just means relative dominance compared to the second best
        return Result.match(best_song_id, confidence)







