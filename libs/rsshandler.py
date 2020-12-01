from .article import Article

class RSSHandler:
    def __init__(self):
        self.__URL = ''
        self.__websiteContent = ''
        self.__responeCode = ''
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
        for child in channel:
            if child.tag == 'title':
                print(child.text)
            elif child.tag == 'link':
                print(child.text)
            elif child.tag == 'description':
                print(child.text)
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
        

    def returnArticles(self):
        return self.__articles
