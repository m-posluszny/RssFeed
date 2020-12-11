import plyvel
import os 
import shutil
import json

class DatabaseHandler:
    actualDatabase = None
    actualDatabasePath = ''
    dbIsTemp = False

    # TODO(mateusz): Read about cross platform home directory and use it to create
    # the database
    @staticmethod
    def __createDatabase(path):
        if not os.path.exists(path):
            os.makedirs(path)
        DatabaseHandler.actualDatabase = plyvel.DB(path, create_if_missing=True)
        DatabaseHandler.actualDatabasePath = path

    @staticmethod
    def destroyDatabase():
        del DatabaseHandler.actualDatabase
        plyvel.destroy_db(DatabaseHandler.actualDatabasePath)
        DatabaseHandler.actualDatabase = None
        DatabaseHandler.actualDatabasePath = ''
        DatabaseHandler.dbIsTemp = False

    @property
    def databaseOnline(self):
        return not DatabaseHandler.actualDatabase.closed

    def __init__(self, db_path = './tmp/', dbIsTemp = False):
        if DatabaseHandler.actualDatabase == None:
            DatabaseHandler.dbIsTemp = dbIsTemp
            DatabaseHandler.__createDatabase(db_path)

    def addEntry(self, key, value):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        if isinstance(value, str):
            value = value.encode()
            assert(isinstance(value, bytes))

        DatabaseHandler.actualDatabase.put(key, value)

    def getEntry(self, key):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = DatabaseHandler.actualDatabase.get(key)
        if value == None:
            return None
        else:
            return json.loads(value)

    def deleteEntry(self, key):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        return DatabaseHandler.actualDatabase.delete(key)
