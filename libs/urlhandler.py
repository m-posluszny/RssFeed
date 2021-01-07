from libs.grouphandler import GroupHandler
import re
from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler

class URLHandler:
    popular_name ="Most Popular URLs"

    @staticmethod
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
        dbh.addEntry(username, res)
        stats = dbh.getEntry("__all_urls_statistics__")
        if stats == None:
            stats = []
            stats.append([url,1])
            dbh.addEntry("__all_urls_statistics__",stats)
            return
        url_exists=False
        for i,stat in enumerate(stats):
            if url in stat:
                url_exists=True
                stats[i][1]+=1
                break
        if not url_exists:
            stats.append([url,1])
        dbh.addEntry("__all_urls_statistics__",stats)

    @staticmethod
    def addURLToGroup(url, group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                if group in res['groups']:
                    if i not in res['groups'][group]:
                        res['groups'][group].append(i)
                else:
                    res['groups'][group] = [i] 

                dbh.addEntry(username, res)
                return i

    @staticmethod
    def removeURL(url):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                res['urls'].pop(i)

                for j, group in enumerate(res['groups']):
                    if i in res['groups'][group]:
                        hl = res['groups'][group][:i]
                        hr = list(map(lambda x: x - 1, res['groups'][group][i + 1:]))
                        res['groups'][group] = hl + hr

                dbh.addEntry(username, res)
                stats = dbh.getEntry("__all_urls_statistics__")
                if stats == None:
                    return
                url_exists=False
                for i,stat in enumerate(stats):
                    if url in stat:
                        url_exists=True
                        stats[i][1]-=1
                        break
                if url_exists and stats[i][1] == 0:
                    stats.pop(i)
                dbh.addEntry("__all_urls_statistics__",stats)
                return

    @staticmethod
    def removeURLFromGroup(url, group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                if group in res['groups'] and i < len(res['groups'][group]):
                    res['groups'][group].remove(i)
                    dbh.addEntry(username, res)

                return

    @staticmethod
    def appendDownloadedArticles(url, articles):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                for nart in articles:
                    addThisUrl = True
                    for eart in entry['articles']:
                        if eart['title'] == nart.title:
                            addThisUrl = False
                            break
                    
                    if addThisUrl:
                        nentry = {
                                "title": nart.title,
                                "link": nart.link,
                                "desc": nart.content,
                                "pub_date": nart.pubDate,
                                "pub_date_parsed": nart.pubDateParsed,
                                "seen": False,
                                }

                        entry['articles'].append(nentry)

        dbh.addEntry(username, res)

    @staticmethod
    def setArticleSeen(url, seen):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.getEntry(username)

        for i, entry in enumerate(res['urls']):
            for j, article in enumerate(entry['articles']):
                if article['link'] == url:
                    res['urls'][i]['articles'][j]['seen'] = seen
                    break

        dbh.addEntry(username, res)

    @staticmethod
    def getMostPopularURLs():
        dbh = DatabaseHandler()
        groups = GroupHandler()
        user= dbh.getEntry(CredentialsHandler.lastUsername)
        if URLHandler.popular_name in user["groups"]:
            groups.removeGroup(URLHandler.popular_name)
        groups.addGroup(URLHandler.popular_name)
        mostpopular = dbh.filterList()
        add_to_user_urls=True
        indexes = []
        for stat in mostpopular:
            url = stat[0]
            idx = 0
            for user_url in user["urls"]:
                if user_url["actual_url"] == url:
                    add_to_user_urls=False
                    idx +=1
            if add_to_user_urls:
                idx = URLHandler.addURL(url)                
            indexes.append(idx)
            URLHandler.addURLToGroup(url,URLHandler.popular_name)
        return mostpopular,indexes

    @staticmethod
    def stringIsURL(url):
        regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        res = re.match(regex, url) is not None

        return res
