from sys import exit
from app.models.player import Player
from app.controllers.mongo_controller import MongoController


class MainController:

    CONST_SONG_MENU = "{0}. Title: {1}, Artist: {2}, Link: {3}"

    def __init__(self):
        self.starter = Player()  # a var that sets up the player class for later use.
        self.queue_builder = []
        # Connect to MongoDB.
        self.mongodb = MongoController("localhost", "27017", "admin", "pa55word")
        # Get all the songs from the database.
        self.songs = self.mongodb.get_all_songs()

    @staticmethod
    def options(self, songs):
        self.print_songs(songs)

    @staticmethod
    def print_songs(songs):
        count = 1
        for song in songs:
            print(MainController.CONST_SONG_MENU.format(count, song.get_title(), song.get_artist(), song.get_link()))
            count += 1

    def removal_list(self, queue):
        for song in queue:
            self.queue_builder.append(song)
        self.print_songs(self.queue_builder)

    @staticmethod
    def not_valid():
        print("That is not a valid choice.")
        print("")

    def main(self):
        print("")
        print("Welcome to the main menu please select a option:")
        print("1. Play a song.")
        print("2. Create and play a playlist.")
        print("3. Power off.")
        print("")

        action = input("> ")

        if action == '1':
            return self.play()

        elif action == '2':
            return self.queue()

        elif action == '3':
            print("Powering off, have a nice day.")
            return self.off()

        else:
            self.not_valid()
            return self.main()

    @staticmethod
    def off():
        return exit(1)

    def play(self):
        print("")
        print("Which song do you want to play:")
        self.options(self, self.songs)
        print("")
        print("type main to go back to main menu")
        print("")

        action = input("> ")

        if action.isdigit():
            num = int(action)
            length = len(self.songs)
            if num <= length:
                num -= 1
                self.starter.play(self.songs[num])
                print("")
                return self.again()

        elif action == "main":
            return self.main()

        else:
            self.not_valid()
            return self.play()

    def again(self):
        print("")
        print("Play another song? (Y/N)")
        print("Note: selecting no(N) will power off the system.")
        print("Typing in 'main' will bring you back to the main menu")
        print("")

        action = input("> ")
        action.lower()

        if action == 'y':
            return self.play()

        elif action == 'n':
            print("Powering off, have a nice day.")
            return self.off()

        elif action == 'main':
            return self.main()

        else:
            self.not_valid()
            return self.again()

    def queue(self):
        print("")
        print("The playlist is currently empty.")
        print("Which song do you want to add to the playlist?")
        self.options(self, self.songs)
        print("")
        print("type main to go back to main menu")
        print("")

        action = input("> ")
        action.lower()

        if action.isdigit():
            num = int(action)
            length = len(self.songs)
            if num <= length:
                num -= 1
                self.starter.add(self.songs[num])
                print("")
                return self.playlist()

        elif action == 'main':
            return self.main()

        else:
            self.not_valid()
            return self.queue()

    def playlist(self):
        print("")
        print("Current song(s) in playlist:")
        self.options(self, self.starter.queue)
        print("")
        print("Would you like to 'play' the list now? type in 'play'.")
        print("If you want to add more songs, type in 'add'.")
        print("If you want to remove a song, type in 'remove'.")
        print("If you want to return to the main menu, type in 'main'.")
        print("Note: If you return to main menu, your playlist will be deleted.")
        print("")

        action = input("> ")
        action.lower()

        if action == 'main':
            self.starter.queue.clear()
            return self.main()

        elif action == 'play':
            return self.queue_play()

        elif action == 'add':
            return self.add()

        elif action == 'remove':
            return self.remove()

        else:
            self.not_valid()
            return self.playlist()

    def add(self):
        print("")
        print("Which other song do you want to add?")
        self.options(self, self.songs)
        print("")
        print("type in main to return to main menu, also discards your playlist.")
        print("note: repeated songs will not be played or added, only add one of each.")
        print("")

        action = input("> ")
        action.lower()

        if action.isdigit():
            num = int(action)
            length = len(self.songs)
            if num <= length:
                num -= 1
                self.starter.add(self.songs[num])
                print("")
                return self.playlist()

        elif action == 'main':
            self.starter.queue.clear()
            del self.queue_builder[:]
            return self.main()

        else:
            self.not_valid()
            return self.add()

    def remove(self):
        print("")
        print("Which song do you want to remove?")
        if len(self.starter.queue) == 0:
            print("The playlist is empty returning to main.")
            print("")
            return self.main()
        else:
            self.removal_list(self.starter.queue)
        print("")
        print("Type 'play' to play the current playlist.")
        print("Type 'add' to add songs to the playlist.")
        print("Type 'main' to return to the main menu.")
        print("note: returning to the main menu will discard your playlist.")
        print("")

        action = input("> ")
        action.lower()

        if action.isdigit():
            num = int(action)
            length = len(self.starter.queue)
            if num <= length:
                num -= 1
                self.starter.remove(self.queue_builder[num])
                del self.queue_builder[:]
                return self.remove()

        elif action == 'main':
            self.starter.queue.clear()
            del self.queue_builder[:]
            return self.main()

        elif action == 'play':
            del self.queue_builder[:]
            return self.queue_play()

        elif action == 'add':
            del self.queue_builder[:]
            return self.add()

        else:
            self.not_valid()
            del self.queue_builder[:]
            return self.remove()

    def queue_play(self):
        self.starter.queue_play()
        print("")
        print("If you want to play the songlist again type in 'play'")
        print("If you want to return to the main menu type in 'main'")
        print("Note: returning to the main menu will erase your playlist.")
        print("")

        action = input("> ")
        action.lower()

        if action == 'play':
            return self.queue_play()

        elif action == 'main':
            del self.queue_builder[:]
            self.starter.queue.clear()
            return self.main()

        else:
            self.not_valid()
            del self.queue_builder[:]
            return self.queue_play_options()

    def queue_play_options(self):
        print("")
        print("If you want to play the song list again, type in 'play'")
        print("If you want to return to the main menu, type in 'main'")
        print("Note: returning to the main menu will erase your playlist.")
        action = input("> ")
        action.lower()

        if action == 'play':
            return self.queue_play()

        elif action == 'main':
            del self.queue_builder[:]
            self.starter.queue.clear()
            return self.main()

        else:
            self.not_valid()
            del self.queue_builder[:]
            return self.queue_play_options()