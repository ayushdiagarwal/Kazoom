class Result:
    """
    Represents the outcome of a matching operation.

    Invariants:
    - song_id == -1  -> no match, confidence must be 0
    - song_id >= 0   -> valid match, confidence in (0, 100]
    """

    def __init__(self, song_id: int, confidence: float):
        if song_id < -1:
            raise ValueError("song_id must be >= -1")

        if not (0.0 <= confidence <= 100.0):
            raise ValueError("confidence must be between 0 and 100")

        if song_id == -1 and confidence != 0.0:
            raise ValueError("no-match result must have confidence 0")

        self._song_id = song_id
        self._confidence = confidence

    @property
    def song_id(self) -> int:
        return self._song_id

    @property
    def confidence(self) -> float:
        return self._confidence

    @property
    def found(self) -> bool:
        return self._song_id != -1

    @classmethod
    def match(cls, song_id: int, confidence: float) -> "Result":
        return cls(song_id=song_id, confidence=confidence)

    @classmethod
    def no_match(cls) -> "Result":
        return cls(song_id=-1, confidence=0.0)