import re
import json
from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler

class URLHandler:
    def addURL(url):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for entry in res['urls']:
            if entry['actual_url'] == url:
                return

        new_entry = {
                'actual_url': url,
                'rss_title': None,
                'rss_link': None,
                'rss_desc': None,
                'articles': [],
                }

        res['urls'].append(new_entry)
        dbh.addEntry(username, json.dumps(res))

    def addURLToGroup(url, group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                if group in res['groups']:
                    res['groups'][group].append(i)
                else:
                    res['groups'][group] = [i] 

                dbh.addEntry(username, json.dumps(res))
                return

    def removeURL(url):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                res['urls'].pop(i)

                for j, group in enumerate(res['groups']):
                    print(res['groups'][group])
                    if i in res['groups'][group]:
                        res['groups'][group].remove(i)

                dbh.addEntry(username, json.dumps(res))

                return

    def removeURLFromGroup(url, group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                if group in res['groups']:
                    res['groups'][group].remove(i)
                    dbh.addEntry(username, json.dumps(res))

                return

    def getMostPopularURLs():
        pass

    def stringIsURL(self, url):
        regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        res = re.match(regex, url) is not None

        return res
