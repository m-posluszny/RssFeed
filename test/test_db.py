import unittest
from libs.databasehandler import DatabaseHandler


class TestURLHandler(unittest.TestCase):

    def test_basic_operations(self):
        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)

        db.add_entry('testkey', 'testvalue')

        res = db.get_entry('testkey')
        self.assertEqual(res, 'testvalue')

        res = db.delete_entry('testkey')
        self.assertEqual(res, True)

        res = db.get_entry('nonvalidtestkey')
        self.assertEqual(res, None)

        DatabaseHandler.destroy_database()

    def test_pickle_storing(self):
        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)

        l = [str(i) for i in range(100)]
        db.add_entry('testkey', l)

        res = db.get_entry('testkey')
        self.assertNotEqual(res, None)

        self.assertEqual(res, l)

        DatabaseHandler.destroy_database()
