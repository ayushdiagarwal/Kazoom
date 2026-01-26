class Fingerprint:

    def __init__(self, hash_val:int, anchor_time:float, song_id:int = -1):

        if anchor_time < 0:
            raise ValueError("Anchor time needs to be positive")

        if song_id < 0:
            raise ValueError("Song id neds to be positive")

        self._hash_val = hash_val
        self._anchor_time = anchor_time
        self._song_id = song_id

    @property
    def hash_val(self):
        return self._hash_val
    
    @property
    def song_id(self):
        return self._song_id
    
    @property
    def anchor_time(self):
        return self._anchor_time
    
    def __repr__(self):
        return f"Fingerprint(hash={self._hash}, t={self._anchor_time:.3f}, song={self._song_id})"
