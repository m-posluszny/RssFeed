import unittest
from libs.credhandler import CredentialsHandler

class TestURLHandler(unittest.TestCase):

    def test_hashes_empty(self):
        credh = CredentialsHandler('testusername', '')

        credh.encryptCredentials()
        self.assertEqual(credh.password, 'da39a3ee5e6b4b0d3255bfef95601890afd80709')

    def test_hashes_empty_bytes(self):
        credh = CredentialsHandler('testusername', b'')

        credh.encryptCredentials()
        self.assertEqual(credh.password, 'da39a3ee5e6b4b0d3255bfef95601890afd80709')

    def test_hashes_nonempty(self):
        credh = CredentialsHandler('testusername', 'nonemptytestpassword')

        credh.encryptCredentials()
        self.assertEqual(credh.password, '3217aa106d566c22fb0f2e44af0e28d024d4fa98')

    def test_hashes_nonempty_bytes(self):
        credh = CredentialsHandler('testusername', b'nonemptytestpassword')

        credh.encryptCredentials()
        self.assertEqual(credh.password, '3217aa106d566c22fb0f2e44af0e28d024d4fa98')

    def test_credentials_validation(self):
        credh = CredentialsHandler('testusername', b'nonemptytestpassword')

        credh.encryptCredentials()
        # Until we have no database connected here this will always pass, if it fails
        # rewrite the test in a way it's taking into consideration the database
        self.assertEqual(credh.areCredValid(), False)
