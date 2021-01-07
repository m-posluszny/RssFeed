import lmdb
import os
import shutil
import pickle


class DatabaseHandler:
    actualDatabase = None
    actualDatabasePath = ''
    dbIsTemp = False

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

    def __init__(self, db_path='./tmp/', dbIsTemp=False):
        if DatabaseHandler.actualDatabase == None:
            DatabaseHandler.dbIsTemp = dbIsTemp
            DatabaseHandler.__createDatabase(db_path)

    def addEntry(self, key, value):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = pickle.dumps(value)
        self.addEntryBytes(key, value)

    def addEntryBytes(self, key, value):
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
            return pickle.loads(value)

    def deleteEntry(self, key):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = None
        with DatabaseHandler.actualDatabase.begin(write=True) as outTxn:
            value = outTxn.delete(key)
        return value

    def filterList(self):
        stats = self.getEntry("__all_urls_statistics__")
        if not stats:
            return []
        stats.sort(reverse=True, key=lambda entry: entry[1])
        self.addEntry("__all_urls_statistics__",stats)
        if len(stats)>5:
            return stats[:5]
        return stats
                    
    
    def printEntry(self, key):
        res = self.getEntry(key)

        print(key, res)
