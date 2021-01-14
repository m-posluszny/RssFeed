from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler


class GroupHandler:
    @staticmethod
    def add_group(group):
        """
        Add group to the database if one doesn't exists

        Args:
            group (string): name of the group

        Returns:
            bool: True if group has been added succesfully
        """
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        if any([entry for entry in res['groups'] if group in entry]):
            return False

        res['groups'][group] = []
        dbh.add_entry(username, res)
        return True

    @staticmethod
    def remove_group(group):
        """
        Remove group from the database

        Args:
            group (string): name of the group

        Returns:
            bool: True if group has been removed succesfully
        """
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for i, entry in enumerate(res['groups']):
            if group in entry:
                res['groups'].pop(group)
                dbh.add_entry(username, res)
                return True
        return False
