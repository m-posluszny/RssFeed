import unittest
from libs.databasehandler import DatabaseHandler

class TestURLHandler(unittest.TestCase):

    def test_basic_operations(self):
        db = DatabaseHandler(db_path = "pytests/", dbIsTemp = True)

        db.addEntry('testkey', '\"testvalue\"')

        res = db.getEntry('testkey')
        self.assertEqual(res, "testvalue")

        res = db.deleteEntry('testkey')
        self.assertEqual(res, True)

        res = db.getEntry('nonvalidtestkey')
        self.assertEqual(res, None)

        DatabaseHandler.destroyDatabase()

    def test_json_storing(self):
        import json
        db = DatabaseHandler(db_path = "pytests/", dbIsTemp = True)

        l = [str(i) for i in range(100)]
        asStr = json.dumps(l)

        db.addEntry('testkey', asStr)

        res = db.getEntry('testkey')
        self.assertNotEqual(res, None)

        self.assertEqual(res, l)

        DatabaseHandler.destroyDatabase()
