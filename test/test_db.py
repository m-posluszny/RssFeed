import unittest
from libs.databasehandler import DatabaseHandler

class TestURLHandler(unittest.TestCase):

    def test_empty_handler(self):
        db = DatabaseHandler()

        self.assertEqual(db.databaseOnline, True)

    def test_inserting_values(self):
        db = DatabaseHandler()

        db.addEntry('testkey', 'testvalue')

        self.assertEqual(db.databaseOnline, True)

        res = db.getEntry('testkey')
        self.assertEqual(res, b'testvalue')

        res = db.getEntry('nonvalidtestkey')
        self.assertEqual(res, None)
