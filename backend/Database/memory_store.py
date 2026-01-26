from collections import defaultdict
from Fingerprint.fingerprint import Fingerprint
from Database.base import FingerprintStore

class InMemoryFingerprintStore(FingerprintStore):
    """
    In-memory fingeprint store using a dictionary
    """

    def __init__(self):
        self._store: dict[int, list[FingerprintStore]] = defaultdict(list)

    def insert(self, fingerprint: Fingerprint) -> None:
        self._store[fingerprint.hash].append(fingerprint)

    def lookup(self, hash_val:int) -> list[Fingerprint]:
        return self._store.get(hash_val, [])