from .article import Article
from libs.rss import RSSHeader

class RSSHandler:
    def __init__(self):
        self.__URL = ''
        self.__websiteContent = ''
        self.__responseCode = 0
        self.__rssHeader = RSSHeader()
        self.__articles = []

    def retriveDataFromURL(self, url):
        import requests

        self.__URL = url

        response = requests.get(url)
        self.__websiteContent = response.text
        self.__responseCode = response.status_code

    def formData(self):
        pass

    def parseXML(self):
        import feedparser

        parsed = feedparser.parse(self.__websiteContent)


        rssFeed = parsed['feed']
        assert('title' in rssFeed)
        assert('link' in rssFeed)
        assert('subtitle' in rssFeed)

        rssTitle, rssLink, rssDesc = rssFeed['title'], rssFeed['link'], rssFeed['subtitle']
        self.__rssHeader = RSSHeader(rssTitle, rssLink, rssDesc)

        rssItems = parsed['entries']
        for item in rssItems:
            assert('title' in item)
            assert('link' in item)
            assert('summary' in item)
            assert('published' in item)

            self.__articles.append(Article(item['title'], item['link'], item['summary'], item['published']))

    def returnArticles(self):
        return self.__articles

    def returnRSSHeader(self):
        return ()

    # This is for debugging purposes?
    # I have it in vpp, but did not include that in sequence diagram
    def fetchIsSuccess(self):
        success = self.__responseCode >= 200 and self.__responseCode <= 299
        return success
