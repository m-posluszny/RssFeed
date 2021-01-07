from libs.rss import RSSHeader


class Article:
    def __init__(self, title, link, desc, date, dateParsed):
        self.__header = RSSHeader(title, link, desc)
        self.__date = date
        self.__dateParsed = dateParsed

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

    @property
    def pubDate(self):
        return self.__date

    @property
    def pubDateParsed(self):
        return self.__dateParsed
