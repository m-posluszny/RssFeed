import plyvel


class DatabaseHandler:
    actualDatabase = None

    # TODO(mateusz): Read about cross platform home directory and use it to create
    # the database
    def __createDatabase():
        DatabaseHandler.actualDatabase = plyvel.DB('/tmp/testdb/', create_if_missing=True)

    @property
    def databaseOnline(self):
        return not DatabaseHandler.actualDatabase.closed

    def __init__(self):
        if DatabaseHandler.actualDatabase == None:
            DatabaseHandler.__createDatabase()

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

        return db.get(key)

    def deleteEntry(self, key):
        db = DatabaseHandler.actualDatabase

        if isinstance(key, str):
            key = key.encode()
            assert(isinstance(key, bytes))

        return db.delete(key)
