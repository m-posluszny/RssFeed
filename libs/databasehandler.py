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
    def __createDatabase(path):
        if not os.path.exists(path):
            os.makedirs(path)
        DatabaseHandler.actualDatabase = plyvel.DB(path, create_if_missing=True)
        DatabaseHandler.actualDatabasePath = path

    def __destroyDatabase():
        del DatabaseHandler.actualDatabase
        plyvel.destroy_db(DatabaseHandler.actualDatabasePath)
        DatabaseHandler.actualDatabase = None
        DatabaseHandler.actualDatabasePath = ''

    @property
    def databaseOnline(self):
        return not DatabaseHandler.actualDatabase.closed

    def __init__(self, db_path = './tmp/', dbIsTemp = False):
        if DatabaseHandler.actualDatabase == None:
            DatabaseHandler.dbIsTemp = dbIsTemp
            DatabaseHandler.__createDatabase(db_path)

    def __del__(self):
        if DatabaseHandler.dbIsTemp:
            DatabaseHandler.__destroyDatabase()

    def addEntry(self, key, value):
        db = DatabaseHandler.actualDatabase

        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        if isinstance(value, str):
            value = value.encode()
            assert(isinstance(value, bytes))

        db.put(key, value)

    def getEntry(self, key):
        db = DatabaseHandler.actualDatabase

        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = db.get(key)
        if value == None:
            return None
        else:
            return json.loads(value)

    def deleteEntry(self, key):
        db = DatabaseHandler.actualDatabase

        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        return db.delete(key)
