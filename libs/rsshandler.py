from .article import Article
from libs.rss import RSSHeader
import feedparser
import time
import requests


class RSSHandler:
    def __init__(self):
        self.__URL = ""
        self.__websiteContent = ""
        self.__responseCode = 0
        self.__rssHeader = RSSHeader()
        self.__articles = []

    def fetch_from_url(self, url):
        """
        Gets website content from given url

        Args:
            url (string): url to site with rss.xml
        """
        self.__URL = url
        try:
            response = requests.get(url)
            self.__websiteContent = response.text
            self.__responseCode = response.status_code
        except:
            self.__responseCode = 400
            print("cannot fetch", url)

    def parse_xml(self):
        """
        This method parse __webisteContent getting all rss data from it 
        """
        parsed = feedparser.parse(self.__websiteContent)

        rssFeed = parsed["feed"]
        rssTitle = rssFeed["title"] if "title" in rssFeed else ""
        rssLink = rssFeed["link"] if "link" in rssFeed else ""
        rssDesc = rssFeed["subtitle"] if "subtitle" in rssFeed else ""
        self.__rssHeader = RSSHeader(rssTitle, rssLink, rssDesc)

        rssItems = parsed["entries"]
        for item in rssItems:
            itemTitle = item["title"] if "title" in item else "null title"
            itemLink = item["link"] if "link" in item else "null link"
            itemSumm = item["summary"] if "summary" in item else "null summary"
            itemPub = item["published"] if "published" in item else "null pubdate"
            itemPubParsed = item["published_parsed"] if "published_parsed" in item else time.localtime(
                0)

            self.__articles.append(
                Article(itemTitle, itemLink, itemSumm, itemPub, itemPubParsed))

    def return_articles(self):
        """
        This method returns article previously parsed
        Returns:
            List: List of articles
        """
        return self.__articles

    def fetch_is_success(self):
        """
        This method checks responseCode and returns true if it is in range 200-299
        Returns:
            Bool: True or False depends on reponse code
        """
        success = self.__responseCode >= 200 and self.__responseCode <= 299
        return success
