from Fingerprint.fingerprint import Fingerprint
from abc import abstractmethod, ABC

class FingerprintStore(ABC):

    @abstractmethod
    def insert(self, fingerprint:Fingerprint):
        """Store a single fingerprint"""
        pass

    @abstractmethod
    def lookup(self, hash_val:int) -> list[Fingerprint]:
        """Return all fingerprints matching a given hash"""
        pass

    