from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler
import json

class GroupHandler:
    @staticmethod
    def addGroup(group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        if any([entry for entry in res['groups'] if group in entry]):
            return

        res['groups'][group] = []
        dbh.addEntry(username, json.dumps(res))

    @staticmethod
    def removeGroup(group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['groups']):
            if group in entry:
                res['groups'].pop(group)
                dbh.addEntry(username, json.dumps(res))
                return
