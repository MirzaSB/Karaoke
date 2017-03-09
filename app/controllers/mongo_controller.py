from pymongo import MongoClient, errors
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

    def __init__(self, db_host, db_port, username, password, **kwargs):
        """
        A constructor that connects to MongoDB, and sets up the "songs" collection.

        :param db_host: str: The MongoDB host.
        :param db_port: int: The MongoDB port.
        :param username: str: The username used to authenticate MongoDB.
        :param password: str: The password used to authenticate MongoDB.
        :param kwargs: For super class purposes only.
        """
        super().__init__(**kwargs)
        self.username = username
        self.password = password
        self.dbHost = db_host
        self.dbPort = db_port
        # Connect to the "karaoke" database.
        self.client = MongoController.connect(self)
        # Setup the "songs" collection.
        self.songsCollection = self.client.songs
        # Add indexes for "artist" and "title" properties.
        self.songsCollection.create_index([(self.CONST_PROPERTY_ARTIST, 1),
                                           (self.CONST_PROPERTY_TITLE, 1)], default_language='english')

    def connect(self):
        """
        Connects to the "karaoke" database.

        :return: MongoClient: The established connection to the "karaoke" database.
        """
        try:
            # Initialize a MongoClient instance, and connect to the database.
            connection_string = "mongodb://{0}:{1}@{2}:{3}" \
                .format(self.username, self.password, self.dbHost, self.dbPort)
            self.client = MongoClient(connection_string)
            # Return the connection instance.
            return self.client[self.CONST_DB_NAME]
        except errors.ServerSelectionTimeoutError as e:
            print("Could not connect to MongoDB. The exception message is below:")
            print(e)

    def get_all_songs(self):
        """
        Returns all the songs from the database.

        :return: list: A list containing all the Song objects (transformed documents from the 'songs' collection).
        """
        # Initialize a new list to store the processed Song objects.
        songs = []
        # Get all the documents from the "songs" collection.
        docs = self.songsCollection.find()
        # For each document found, transform it into a Song object.
        for doc in docs:
            # Store the transformed Song object into the list.
            songs.append(self.transform_doc_to_song(doc))
        # Return the list of Song objects.
        return songs

    def get_song(self, title, artist):
        """
        Returns a song from MongoDB.

        :param title: str: The "title" value of the song.
        :param artist: str: The "artist" value of the song.
        :return: Song: The transformed song object from MongoDB.
        """
        # Get the song from MongoDB.
        song_json = self.songsCollection.find_one({self.CONST_PROPERTY_TITLE: title,
                                                   self.CONST_PROPERTY_ARTIST: artist})
        if song_json is None:
            print("No song found.")
            return
        # Transform the returned dictionary object to a song, and return it.
        transformed_song = self.transform_doc_to_song(song_json)
        return transformed_song

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

    def insert_song_object(self, song_obj):
        """
        Inserts a Song object into MongoDB.

        :param song_obj: Song: The song object to insert.
        :return: str: The "_id" value of the inserted song. If the song could not be entered, then "None" is returned.
        """
        if isinstance(song_obj, Song):
            return self.insert_song(song_obj.get_title(), song_obj.get_artist(), song_obj.get_link())
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
        deleted_result = self.songsCollection.delete_one({self.CONST_PROPERTY_TITLE: title,
                                                         self.CONST_PROPERTY_ARTIST: artist})
        deleted_count = deleted_result.deleted_count
        if deleted_count == 0:
            print("The song of the 'title' value, '%s' is not in MongoDB and hence could not be deleted." % title)
        else:
            print("The song of the '_id' value, '%s' was found in MongoDB and successfully deleted." % title)
        # Return the DeletedResult object.
        return deleted_result

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
