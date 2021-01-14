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
        """Creates local file for database

        Args:
            path (string): path to database
        """
        if not os.path.exists(path):
            os.makedirs(path)
        DatabaseHandler.actualDatabase = lmdb.open(path)
        DatabaseHandler.actualDatabasePath = path

    @staticmethod
    def destroy_database():
        """
        Removes database
        Made for testing purposes
        """
        del DatabaseHandler.actualDatabase
        DatabaseHandler.actualDatabase = None
        if os.path.exists(DatabaseHandler.actualDatabasePath):
            shutil.rmtree(DatabaseHandler.actualDatabasePath)
        DatabaseHandler.actualDatabasePath = ''
        DatabaseHandler.dbIsTemp = False

    def __init__(self, db_path='./tmp/', dbIsTemp=False):
        """
        Constructor, wchich creates database if one doesn't exists

        Args:
            db_path (str, optional): Location for creating database. Defaults to './tmp/'.
            dbIsTemp (bool, optional): Parameter used for testing. Defaults to False.
        """
        if DatabaseHandler.actualDatabase == None:
            DatabaseHandler.dbIsTemp = dbIsTemp
            DatabaseHandler.__create_database(db_path)

    def add_entry(self, key, value):
        """
        Add entry to database in key:value model

        Args:
            key (string)
            value (dict)
        """
        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        value = pickle.dumps(value)
        self.add_entry_bytes(key, value)

    def add_entry_bytes(self, key, value):
        """
        Add entry to database in byte format 

         Args:
            key (string)
            value (dict)
        """
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
        """
        Filter urls list and gets top 5 most viewed rss urls

        Returns:
            list: list of 5 most popular url objects
        """
        stats = self.get_entry("__all_urls_statistics__")
        if not stats:
            return []
        stats.sort(reverse=True, key=lambda entry: entry[1])
        self.add_entry("__all_urls_statistics__", stats)
        if len(stats) > 5:
            return stats[:5]
        return stats

    def print_entry(self, key):
        """
        Used for testing purposes to display database content

        Args:
            key (string)
        """
        res = self.get_entry(key)
        print(key, res)
