import lmdb
import os
import shutil
import pickle


class DatabaseHandler:
    actualDatabase = None
    actualDatabasePath = ''
    dbIsTemp = False

    @staticmethod
    def __create_database(path):
        if not os.path.exists(path):
            os.makedirs(path)
        DatabaseHandler.actualDatabase = lmdb.open(path)
        DatabaseHandler.actualDatabasePath = path

    @staticmethod
    def destroy_database():
        del DatabaseHandler.actualDatabase
        DatabaseHandler.actualDatabase = None
        if os.path.exists(DatabaseHandler.actualDatabasePath):
            shutil.rmtree(DatabaseHandler.actualDatabasePath)
        DatabaseHandler.actualDatabasePath = ''
        DatabaseHandler.dbIsTemp = False

    def __init__(self, db_path='./tmp/', dbIsTemp=False):
        if DatabaseHandler.actualDatabase == None:
            DatabaseHandler.dbIsTemp = dbIsTemp
            DatabaseHandler.__create_database(db_path)

    def add_entry(self, key, value):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = pickle.dumps(value)
        self.add_entry_bytes(key, value)

    def add_entry_bytes(self, key, value):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        if isinstance(value, str):
            value = value.encode()
            assert(isinstance(value, bytes))

        with DatabaseHandler.actualDatabase.begin(write=True) as inTxn:
            inTxn.put(key, value)

    def get_entry(self, key):
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

    def delete_entry(self, key):
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = None
        with DatabaseHandler.actualDatabase.begin(write=True) as outTxn:
            value = outTxn.delete(key)
        return value

    def filter_list(self):
        stats = self.get_entry("__all_urls_statistics__")
        if not stats:
            return []
        stats.sort(reverse=True, key=lambda entry: entry[1])
        self.add_entry("__all_urls_statistics__", stats)
        if len(stats) > 5:
            return stats[:5]
        return stats

    def print_entry(self, key):
        res = self.get_entry(key)
        print(key, res)
