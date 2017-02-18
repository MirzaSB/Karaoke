from pymongo import MongoClient, errors
from bson.objectid import ObjectId

'''
A class containing all MongoDB methods and utilities.
'''


class MongoController(MongoClient):

    # Constants.
    CONST_DB_NAME = "karaoke"

    # Property Constants.
    CONST_PROPERTY_ARTIST = "artist"
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

    def insert_song(self, artist, title, youtube):
        """
        Inserts a song into the "songs" collection.

        :param artist: str: The "artist" property value.
        :param title: str: The "title" property value.
        :param youtube: str: The "youtube" property value.
        :return: str: The "_id" value of the successfully inserted song from MongoDB.
        """
        # Create a JSON object containing all the "song" properties.
        json = {
            self.CONST_PROPERTY_ARTIST: artist,
            self.CONST_PROPERTY_TITLE: title,
            self.CONST_PROPERTY_YOUTUBE: youtube
        }
        # Store the JSON in MongoDB.
        return self.songsCollection.insert(json)

    def remove_song(self, id):
        """
        Removes a song from the "songs" collection.

        :param id: The "_id" value of the song that is to be removed.
        :return: DeletedResult: The object containing all the deleted document data.
        """
        # Remove the document from MongoDB, and get the "deleted_count" value.
        deletedResult = self.songsCollection.delete_one({'_id': ObjectId(id)})
        deletedCount = deletedResult.deleted_count
        if(deletedCount == 0):
            print("The document of the '_id' value, '%s' is not in MongoDB and hence could not be deleted." % id)
        else:
            print("The document of the '_id' value, '%s' was found in MongoDB and successfully deleted." % id)
        # Return the DeletedResult object.
        return deletedResult

mongo = MongoController("localhost", "27017", "admin", "pa55word")