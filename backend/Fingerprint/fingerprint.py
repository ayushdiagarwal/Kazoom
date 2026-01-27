class Fingerprint:
    """
    Immutable domain object representing a single audio fingerprint.

    A fingerprint encodes the relationship between an anchor peak and a
    target peak as a compact hash value, along with the absolute time of
    the anchor peak. 

    Song_id for a query song would be -1. For everything else, it has to be greater than 0.
    """

    def __init__(self, hash_val:int, anchor_time:float, song_id:int = -1):

        if anchor_time < 0:
            raise ValueError("Anchor time needs to be positive")

        # song_id == -1 represents a query audio
        if song_id < -1:
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
        return f"Fingerprint(hash={self._hash_val}, t={self._anchor_time:.3f}, song={self._song_id})"
