from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler


class GroupHandler:
    @staticmethod
    def add_group(group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        if any([entry for entry in res['groups'] if group in entry]):
            return

        res['groups'][group] = []
        dbh.add_entry(username, res)

    @staticmethod
    def remove_group(group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for i, entry in enumerate(res['groups']):
            if group in entry:
                res['groups'].pop(group)
                dbh.add_entry(username, res)
                return
