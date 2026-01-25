class Peak:

    def __init__(self,freq:float, time:float):

        if time < 0:
            raise ValueError("Time can't be negative")
        
        if freq < 0:
            raise ValueError("Frequency can't be negative")
        
        self._time = time
        self._freq = freq

    @property
    def time(self):
        return self._time
    
    @property
    def freq(self):
        return self._freq
    
    def __repr__(self):
        return f"Peak(time={self._time:.3f}, freq={self._freq:.1f})"
