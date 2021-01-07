import unittest
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler


class TestCredentialsHandler(unittest.TestCase):

    def test_hashes_empty(self):
        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)
        credh = CredentialsHandler('testusername', '')

        credh.encrypt_credentials()
        self.assertEqual(
            credh.password, 'da39a3ee5e6b4b0d3255bfef95601890afd80709')

        DatabaseHandler.destroy_database()

    def test_hashes_empty_bytes(self):
        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)
        credh = CredentialsHandler('testusername', b'')

        credh.encrypt_credentials()
        self.assertEqual(
            credh.password, 'da39a3ee5e6b4b0d3255bfef95601890afd80709')
        DatabaseHandler.destroy_database()

    def test_hashes_nonempty(self):
        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)
        credh = CredentialsHandler('testusername', 'nonemptytestpassword')

        credh.encrypt_credentials()
        self.assertEqual(
            credh.password, '3217aa106d566c22fb0f2e44af0e28d024d4fa98')
        DatabaseHandler.destroy_database()

    def test_hashes_nonempty_bytes(self):
        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)
        credh = CredentialsHandler('testusername', b'nonemptytestpassword')

        credh.encrypt_credentials()
        self.assertEqual(
            credh.password, '3217aa106d566c22fb0f2e44af0e28d024d4fa98')
        DatabaseHandler.destroy_database()

    def test_credentials_validation(self):
        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)
        credh = CredentialsHandler('testusername', b'nonemptytestpassword')

        credh.encrypt_credentials()
        # Until we have no database connected here this will always pass, if it fails
        # rewrite the test in a way it's taking into consideration the database
        self.assertEqual(credh.are_cred_valid(), False)
        DatabaseHandler.destroy_database()

    def test_basic_operations(self):
        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)
        credh = CredentialsHandler('basic_username', 'basic_password')

        credh.encrypt_credentials()

        self.assertEqual(credh.does_user_exist(), False)
        self.assertEqual(credh.are_cred_valid(), False)

        credh.create_user()

        self.assertEqual(credh.does_user_exist(), True)
        self.assertEqual(credh.are_cred_valid(), True)
        DatabaseHandler.destroy_database()
