from libs.rss import RSSHeader

class Article:
    def __init__(self, title, link, desc, date):
        self.__header = RSSHeader(title, link, desc)
        self.__date = date
    def __str__(self):
        return "[{}][{}][{}][{}]".format(self.title, self.__date, self.link, self.content)

    @property
    def title(self):
        return self.__header.title

    @property
    def link(self):
        return self.__header.link

    @property
    def content(self):
        return self.__header.desc
