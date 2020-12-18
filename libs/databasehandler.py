import lmdb
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
        DatabaseHandler.actualDatabase = lmdb.open(path)
        DatabaseHandler.actualDatabasePath = path

    @staticmethod
    def destroyDatabase():
        del DatabaseHandler.actualDatabase
        DatabaseHandler.actualDatabase = None
        if os.path.exists(DatabaseHandler.actualDatabasePath):
            shutil.rmtree(DatabaseHandler.actualDatabasePath)
        DatabaseHandler.actualDatabasePath = ''
        DatabaseHandler.dbIsTemp = False

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

        with DatabaseHandler.actualDatabase.begin(write=True) as inTxn:
            inTxn.put(key, value)

    def getEntry(self, key):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = None
        with DatabaseHandler.actualDatabase.begin(write=True) as outTxn:
            value = outTxn.get(key)
        if value == None:
            return None
        else:
            return json.loads(value)

    def deleteEntry(self, key):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = None
        with DatabaseHandler.actualDatabase.begin(write=True) as outTxn:
            value = outTxn.delete(key)
        return value
    
    def printEntry(self, key):
        res = self.getEntry(key)

        print(key, res)
