class Song:

    def __init__(self, title, artist, youtube):
        self.title = title
        self.artist = artist
        self.youtube = youtube
        self.song = {}
        self.song["title"] = self.title
        self.song["artist"] = self.artist
        self.song["youtube"] = self.youtube

    def get_title(self):
        return self.title

    def get_artist(self):
        return self.artist

    def get_link(self):
        return self.youtube
