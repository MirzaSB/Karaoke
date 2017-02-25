from pymongo import MongoClient, errors, TEXT
from bson.objectid import ObjectId
from app.models.song import Song

'''
A class containing all MongoDB methods and utilities.
'''


class MongoController(MongoClient):

    # Constants.
    CONST_DB_NAME = "karaoke"

    # Property Constants.
    CONST_PROPERTY_ARTIST = "artist"
    CONST_PROPERTY_ID = "_id"
    CONST_PROPERTY_TITLE = "title"
    CONST_PROPERTY_YOUTUBE = "youtube"

    def __init__(self, dbHost, dbPort, username, password, **kwargs):
        """
        A constructor that connects to MongoDB, and sets up the "songs" collection.

        :param dbHost: str: The MongoDB host.
        :param dbPort: int: The MongoDB port.
        :param username: str: The username used to authenticate MongoDB.
        :param password: str: The password used to authenticate MongoDB.
        :param kwargs: For super class purposes only.
        """
        super().__init__(**kwargs)
        self.username = username
        self.password = password
        self.dbHost = dbHost
        self.dbPort = dbPort
        # Connect to the "karaoke" database.
        self.client = MongoController.connect(self)
        # Setup the "songs" collection.
        self.songsCollection = self.client.songs
        # Add indexes for "artist" and "title" properties.
        self.songsCollection.create_index([(self.CONST_PROPERTY_ARTIST, 1),
                                           (self.CONST_PROPERTY_TITLE, 1)],
                                            default_language='english')

    def connect(self):
        """
        Connects to the "karaoke" database.

        :return: MongoClient: The established connection to the "karaoke" database.
        """
        try:
            # Initialize a MongoClient instance, and connect to the database.
            connectionString = "mongodb://{0}:{1}@{2}:{3}".format(self.username, self.password, self.dbHost, self.dbPort)
            self.client = MongoClient(connectionString)
            # Return the connection instance.
            return self.client[self.CONST_DB_NAME]
        except errors.ServerSelectionTimeoutError as e:
            print("Could not connect to MongoDB. The exception message is below:")
            print(e)

    def get_song(self, title, artist):
        """
        Returns a song from MongoDB.

        :param title: str: The "title" value of the song.
        :param artist: str: The "artist" value of the song.
        :return: Song: The transformed song object from MongoDB.
        """
        # Get the song from MongoDB.
        songJson = self.songsCollection.find_one({self.CONST_PROPERTY_TITLE: title,
                                                  self.CONST_PROPERTY_ARTIST: artist})
        if songJson == None:
            print("No song found.")
            return
        # Transform the returned dictionary object to a song, and return it.
        transformedSong = self.transform_doc_to_song(songJson)
        return transformedSong

    def insert_song(self, title, artist, youtube):
        """
        Inserts a song into the "songs" collection.

        :param title: str: The "title" property value.
        :param artist: str: The "artist" property value.
        :param youtube: str: The "youtube" property value.
        :return: str: The "_id" value of the successfully inserted song from MongoDB.
        """
        # Create a JSON object containing all the "song" properties.
        json = {
            self.CONST_PROPERTY_TITLE: title,
            self.CONST_PROPERTY_ARTIST: artist,
            self.CONST_PROPERTY_YOUTUBE: youtube
        }
        # Store the JSON in MongoDB.
        return self.songsCollection.update({self.CONST_PROPERTY_ARTIST: artist,
                                            self.CONST_PROPERTY_TITLE: title},
                                            json, True)

    def insert_song_object(self, songObj):
        """
        Inserts a Song object into MongoDB.

        :param songObj: Song: The song object to insert.
        :return: str: The "_id" value of the inserted song. If the song could not be entered, then "None" is returned.
        """
        if(isinstance(songObj, Song)):
            return self.insert_song(songObj.get_title(), songObj.get_artist(), songObj.get_link())
        else:
            return None

    def remove_song(self, title, artist):
        """
        Removes a song from the "songs" collection.

        :param title: str: The "title" value of the song.
        :param artist: str: The "artist" value of the song.
        :return: DeletedResult: The object containing all the deleted document data.
        """
        # Remove the document from MongoDB, and get the "deleted_count" value.
        deletedResult = self.songsCollection.delete_one({self.CONST_PROPERTY_TITLE: title,
                                                         self.CONST_PROPERTY_ARTIST: artist})
        deletedCount = deletedResult.deleted_count
        if(deletedCount == 0):
            print("The song of the 'title' value, '%s' is not in MongoDB and hence could not be deleted." % title)
        else:
            print("The song of the '_id' value, '%s' was found in MongoDB and successfully deleted." % title)
        # Return the DeletedResult object.
        return deletedResult

    def transform_doc_to_song(self, json):
        """
        Transforms a MongoDB document to a Song object, and returns it.

        :param json: dict: The dictionary object from MongoDB.
        :return: Song: The processed Song object.
        """
        title = json.get(self.CONST_PROPERTY_TITLE)
        artist = json.get(self.CONST_PROPERTY_ARTIST)
        youtube = json.get(self.CONST_PROPERTY_YOUTUBE)
        return Song(title, artist, youtube)

mongo = MongoController("localhost", "27017", "admin3", "pa55word")
mongo.insert_song_object(Song("Safe and Sound", "Capital Cites", "www.youtube.com/watch?v=47dtFZ8CFo8"))
mongo.insert_song_object(Song("In The End", "Linkin Park", "www.youtube.com/watch?v=eVTXPUF4Oz4"))
mongo.insert_song_object(Song("Beautiful Now", "Zedd", "www.youtube.com/watch?v=n1a7o44WxNo"))
