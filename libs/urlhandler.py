from libs.grouphandler import GroupHandler
from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler
from urllib.parse import urlparse


class URLHandler:
    popular_name = "Most Popular URLs"

    @staticmethod
    def add_url(url):
        """
        Adds url to database

        Args:
            url (string): url to rss.xml 

        Returns:
            int: index of newly added url in database
        """
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)
        ret_index = -1
        url_index = -1
        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                url_index = i
                break
        if url_index == -1:
            new_entry = {
                'actual_url': url,
                'rss_title': None,
                'rss_link': None,
                'rss_desc': None,
                'articles': [],
            }

            res['urls'].append(new_entry)
            ret_index = len(res['urls'])-1
            dbh.add_entry(username, res)
        elif url_index in res['groups']['All']:
            return ret_index
        elif url_index not in res['groups']['All']:
            URLHandler.add_url_to_group(url, 'All')
        stats = dbh.get_entry("__all_urls_statistics__")
        if stats == None:
            stats = []
            stats.append([url, 1])
            dbh.add_entry("__all_urls_statistics__", stats)
            return ret_index
        url_exists = False
        for i, stat in enumerate(stats):
            if url in stat:
                url_exists = True
                stats[i][1] += 1
                break
        if not url_exists:
            stats.append([url, 1])
        dbh.add_entry("__all_urls_statistics__", stats)
        return ret_index

    @staticmethod
    def add_url_to_group(url, group):
        """
        Add url to selected group

        Args:
            url (string): selected url
            group (string): name of selected group

        Returns:
            string: Returns index of added url from url list
        """
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
        """
        Removes url from database

        Args:
            url (string): removes url from database
        """
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                for group in res['groups']:
                    if i in res['groups'][group] and group != 'Most Popular URLs':
                        res['groups'][group].remove(i)

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
        """
        Removes url from selected group in database

        Args:
            url ([type]): [description]
            group ([type]): [description]
        """
        dbh = DatabaseHandler()

        username = CredentialsHandler.lastUsername
        res = dbh.get_entry(username)

        for i, entry in enumerate(res['urls']):
            if entry['actual_url'] == url:
                if group in res['groups'] and i in res['groups'][group]:
                    res['groups'][group].remove(i)
                    dbh.add_entry(username, res)

                return

    @staticmethod
    def append_downloaded_articles(url, articles):
        """
        Appends downloaded articles to database

        Args:
            url (string): url to rss
            articles (list): list of articles objects
        """
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
        """
        After reading article this method is used to inform database about
        viwing it

        Args:
            url (string): url to article
            seen (bool): true if article has been seen, otherwise false 
        """
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
        """
        Return list of most popular urls
        In user database that method creates group of most popular urls,
        before creating it checks if one exists, if there is that group
        method deletes it and creates it with fetched list from database

        Returns:
            tuple: tuple contains list of mostpopular urls and indexes of those urls in database
        """
        dbh = DatabaseHandler()
        groups = GroupHandler()
        user = dbh.get_entry(CredentialsHandler.lastUsername)
        if URLHandler.popular_name in user["groups"]:
            groups.remove_group(URLHandler.popular_name)
        groups.add_group(URLHandler.popular_name)
        mostpopular = dbh.filter_list()
        indexes = []
        for stat in mostpopular:
            add_to_user_urls = True
            url = stat[0]
            idx = 0
            for idx, user_url in enumerate(user["urls"]):
                if user_url["actual_url"] == url:
                    add_to_user_urls = False
                    break
            if add_to_user_urls:
                idx = URLHandler.add_url(url)
            indexes.append(idx)
            URLHandler.add_url_to_group(url, URLHandler.popular_name)
        return mostpopular, indexes

    @staticmethod
    def string_is_url(url):
        """
        Checks if string is really a string
        Args:
            url (string): url to rss

        Returns:
            bool: true or false depending of validation of string
        """
        res = urlparse(url)

        hasScheme = len(res.scheme) > 0
        hasNetloc = len(res.netloc) > 0

        if hasScheme and hasNetloc:
            return 'http' in res.scheme
        else:
            return False
