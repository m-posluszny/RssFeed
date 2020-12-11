from hashlib import sha1
from libs.databasehandler import DatabaseHandler

class CredentialsHandler:
    def __init__(self, username, password):

        bytes_passwd = password

        if isinstance(password, str):
            bytes_passwd = password.encode()
        elif not isinstance(password, bytes):
            assert(False)

        self.__username = username
        self.__password = bytes_passwd
        self.__dbHandler = None

    @property
    def password(self):
        return self.__password
    
    @property
    def username(self):
        return self.__username

    def doesUserExist(self):
        dbh = DatabaseHandler()

        result = dbh.getEntry(self.username)

        if result == None:
            return False
        else:
            return True
    
    def createUser(self):
        dbh = DatabaseHandler()

        value = { 'password': self.password }

        result = dbh.addEntry(self.username, value)
        
    def encryptCredentials(self):
        hasher = sha1(self.__password)
        self.__password = hasher.hexdigest()

    def areCredValid(self):
        dbh = DatabaseHandler()

        # Password has to encrypted by this point
        result = dbh.getEntry(self.username)

        if result == None:
            return False
        else:
            if result['password'] == self.password:
                return True
            else:
                return False
