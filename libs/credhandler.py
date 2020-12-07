from hashlib import sha1

class CredentialsHandler:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__dbHandler = None
    
    def doesUserExist(self):
        result = None #obsługa tego będzie musiała być dokładniejsza, sprawdzac czy połączenie moze byc nawiązane
        # result = self.__dbHandler.findEntry(username)
        if result == None:
            return False
        else:
            return True
    
    def createUser(self):
        ... #TODO db send operation
        
    def encryptCredentials(self):
        hasher = sha1(self.__password)
        self.__password = hasher.hexdigest()

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
