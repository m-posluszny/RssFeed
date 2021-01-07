from hashlib import sha1
from libs.databasehandler import DatabaseHandler
import time


class CredentialsHandler:
    lastUsername = ''

    def __init__(self, username, password):

        bytes_passwd = password

        if isinstance(password, str):
            bytes_passwd = password.encode()
        elif not isinstance(password, bytes):
            assert(False)

        self.__username = username
        self.__password = bytes_passwd
        self.__dbHandler = None

        CredentialsHandler.lastUsername = username

    @property
    def password(self):
        return self.__password

    @property
    def username(self):
        return self.__username

    def does_user_exist(self):
        dbh = DatabaseHandler()

        result = dbh.get_entry(self.username)

        if result == None:
            return False
        else:
            return True

    def create_user(self):
        dbh = DatabaseHandler()

        value = {
            'password': self.password,
            'urls': [],
            'groups': {
                'All': [],
            },
        }

        result = dbh.add_entry(self.username, value)

    def encrypt_credentials(self):
        hasher = sha1(self.__password)
        self.__password = hasher.hexdigest()

    def are_cred_valid(self):
        dbh = DatabaseHandler()

        # Password has to encrypted by this point
        result = dbh.get_entry(self.username)

        if result == None:
            return False
        else:
            if result['password'] == self.password:
                return True
            else:
                return False
