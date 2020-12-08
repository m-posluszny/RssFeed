import re

class URLHandler:
    def addURL(url):
        pass

    def addURLToGroup(url, group):
        pass

    def removeURL(url):
        pass

    def removeURLFromGroup(url, group):
        pass

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
