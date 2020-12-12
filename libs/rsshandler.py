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
        import xml.etree.ElementTree as ET
        
        # Root node is <rss> tag
        rss = ET.fromstring(self.__websiteContent)

        # Child of the root node is <channel> which contains the actual data
        channel = rss[0]

        # Channel has to contain <title>, <link>, <description> tags but other are optional 
        # Data for articles is contained inside <item> tags
        # This is bad, I need to redo this one
        rssTitle, rssLink, rssDesc = '', '', ''
        for child in channel:
            if child.tag == 'title':
                rssTitle = child.text
            elif child.tag == 'link':
                rssLink = child.text
            elif child.tag == 'description':
                rssDesc = child.text
            elif child.tag == 'item':
                # Item has to contain the same 3 tags as channel
                # but may contain others
                title = ''
                link = ''
                desc = ''
                date = None
                for ichild in child:
                    if ichild.tag == 'title':
                        title = ichild.text
                    elif ichild.tag == 'link':
                        link = ichild.text
                    elif ichild.tag == 'description':
                        desc = ichild.text
                    elif ichild.tag == 'pubDate':
                        date = ichild.text

                self.__articles.append(Article(title, link, desc, date))

            else:
                print("Unhandled tag", child.tag)
        
        self.__rssHeader = RSSHeader(rssTitle, rssLink, rssDesc)

    def returnArticles(self):
        return self.__articles

    def returnRSSHeader(self):
        return ()

    # This is for debugging purposes?
    # I have it in vpp, but did not include that in sequence diagram
    def fetchIsSuccess(self):
        success = self.__responseCode >= 200 and self.__responseCode <= 299
        return success
