class Player:

    def __init__(self):
        self.queue = set()

    def play(self, song_to_play):
        print("Now playing: '{0}' by {1}, official video at {2}".format
              (song_to_play.get_title(), song_to_play.get_artist(), song_to_play.get_link()))

    def add(self, song):
        self.queue.add(song)
        print("Song '{0}' added to playlist".format(song.get_title()))

    def remove(self, song):
        self.queue.remove(song)
        print("Song '{0}' removed from playlist".format(song.get_title()))

    def queue_play(self):
        for song in self.queue:
            self.play(song)
