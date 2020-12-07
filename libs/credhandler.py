from hashlib import sha1

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

    def doesUserExist(self):
        result = None
        # result = self.__dbHandler.findEntry(username)
        if result == None:
            return False
        else:
            return True
        
    def encryptCredentials(self):
        hasher = sha1(self.__password)
        self.__password = hasher.hexdigest()
        print(self.__password)

    def areCredValid(self):
        # Password has to encrypted by this point
        entry = None

        #entry = self__dbHandler.findEntry(self.__username)

        if entry == None:
            return False
        else:
            if entry.getPassword() == self.__password:
                return True
            else:
                return False
