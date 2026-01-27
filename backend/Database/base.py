from Fingerprint.fingerprint import Fingerprint
from abc import abstractmethod, ABC

class FingerprintStore(ABC):
    """
    Abstract interface for storing and retrieving audio fingerprints. 
    
    This interface is storage-agnostic and is used by higher-level components
    such as matchers to perform fingerprint alignment without knowledge of the
    underlying database or storage mechanism.
    """

    @abstractmethod
    def insert(self, fingerprint:Fingerprint):
        """Store a single fingerprint"""
        pass

    @abstractmethod
    def lookup(self, hash_val:int) -> list[Fingerprint]:
        """Return all fingerprints matching a given hash"""
        pass

    