from libs.grouphandler import GroupHandler
from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler
from urllib.parse import urlparse

class URLHandler:
    popular_name = "Most Popular URLs"

    @staticmethod
    def add_url(url):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for entry in res['urls']:
            if entry['actual_url'] == url:
                return False

        new_entry = {
            'actual_url': url,
            'rss_title': None,
            'rss_link': None,
            'rss_desc': None,
            'articles': [],
        }

        res['urls'].append(new_entry)
        dbh.add_entry(username, res)
        stats = dbh.get_entry("__all_urls_statistics__")
        if stats == None:
            stats = []
            stats.append([url, 1])
            dbh.add_entry("__all_urls_statistics__", stats)
            return True
        url_exists = False
        for i, stat in enumerate(stats):
            if url in stat:
                url_exists = True
                stats[i][1] += 1
                break
        if not url_exists:
            stats.append([url, 1])
        dbh.add_entry("__all_urls_statistics__", stats)
        return True

    @staticmethod
    def add_url_to_group(url, group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                if group in res['groups']:
                    if i not in res['groups'][group]:
                        res['groups'][group].append(i)
                    else:
                        return -1
                else:
                    res['groups'][group] = [i]

                dbh.add_entry(username, res)
                return i

    @staticmethod
    def remove_url(url):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                res['urls'].pop(i)

                for j, group in enumerate(res['groups']):
                    if i in res['groups'][group]:
                        hl = res['groups'][group][:i]
                        hr = list(
                            map(lambda x: x - 1, res['groups'][group][i + 1:]))
                        res['groups'][group] = hl + hr

                dbh.add_entry(username, res)
                stats = dbh.get_entry("__all_urls_statistics__")
                if stats == None:
                    return
                url_exists = False
                for i, stat in enumerate(stats):
                    if url in stat:
                        url_exists = True
                        stats[i][1] -= 1
                        break
                if url_exists and stats[i][1] == 0:
                    stats.pop(i)
                dbh.add_entry("__all_urls_statistics__", stats)
                return

    @staticmethod
    def remove_url_from_group(url, group):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                if group in res['groups'] and i < len(res['groups'][group]):
                    res['groups'][group].remove(i)
                    dbh.add_entry(username, res)

                return

    @staticmethod
    def append_downloaded_articles(url, articles):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

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
                            "pub_date_parsed": nart.pub_date_parsed,
                            "seen": False,
                        }

                        entry['articles'].append(nentry)

        dbh.add_entry(username, res)

    @staticmethod
    def set_article_seen(url, seen):
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for i, entry in enumerate(res['urls']):
            for j, article in enumerate(entry['articles']):
                if article['link'] == url:
                    res['urls'][i]['articles'][j]['seen'] = seen
                    break

        dbh.add_entry(username, res)

    @staticmethod
    def get_most_popular_urls():
        dbh = DatabaseHandler()
        groups = GroupHandler()
        user = dbh.get_entry(CredentialsHandler.lastUsername)
        if URLHandler.popular_name in user["groups"]:
            groups.remove_group(URLHandler.popular_name)
        groups.add_group(URLHandler.popular_name)
        mostpopular = dbh.filter_list()
        add_to_user_urls = True
        indexes = []
        for stat in mostpopular:
            url = stat[0]
            idx = 0
            for user_url in user["urls"]:
                if user_url["actual_url"] == url:
                    add_to_user_urls = False
                    idx += 1
            if add_to_user_urls:
                idx = URLHandler.add_url(url)
            indexes.append(idx)
            URLHandler.add_url_to_group(url, URLHandler.popular_name)
        return mostpopular, indexes

    @staticmethod
    def string_is_url(url):
        res = urlparse(url)

        hasScheme = len(res.scheme) > 0
        hasNetloc = len(res.netloc) > 0

        if hasScheme and hasNetloc:
            return 'http' in res.scheme
        else:
            return False
