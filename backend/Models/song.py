class Song:

    def __init__(self, song_id:int, title:str, artist:str, album:str):
        self._song_id = song_id
        self._title = title
        self._artist = artist
        self._album = album

    @property
    def song_id(self):
        return self._song_id
    
    @property
    def title(self):
        return self._title
    
    @property
    def artist(self):
        return self._artist
    
    @property
    def album(self):
        return self._album