from .article import Article
from libs.rss import RSSHeader
import feedparser


class RSSHandler:
    def __init__(self):
        self.__URL = ""
        self.__websiteContent = ""
        self.__responseCode = 0
        self.__rssHeader = RSSHeader()
        self.__articles = []

    def fetchFromURL(self, url):
        import requests

        self.__URL = url

        try:
            response = requests.get(url)
            self.__websiteContent = response.text
            self.__responseCode = response.status_code
        except:
            self.__responseCode = 400
            print("cannot fetch", url)

    def formData(self):
        pass

    def parseXML(self):
        parsed = feedparser.parse(self.__websiteContent)

        rssFeed = parsed["feed"]
        assert "title" in rssFeed
        assert "link" in rssFeed
        assert "subtitle" in rssFeed

        rssTitle, rssLink, rssDesc = rssFeed["title"], rssFeed["link"], rssFeed["subtitle"]
        self.__rssHeader = RSSHeader(rssTitle, rssLink, rssDesc)

        rssItems = parsed["entries"]
        for item in rssItems:
            assert "title" in item
            assert "link" in item
            assert "summary" in item
            assert "published" in item
            assert "published_parsed" in item

            self.__articles.append(
                Article(item["title"], item["link"], item["summary"],
                        item["published"], item["published_parsed"])
            )

    def returnArticles(self):
        return self.__articles

    def returnRSSHeader(self):
        return ()

    # This is for debugging purposes?
    # I have it in vpp, but did not include that in sequence diagram
    def fetchIsSuccess(self):
        success = self.__responseCode >= 200 and self.__responseCode <= 299
        return success
