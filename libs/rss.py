class RSSHeader:
    def __init__(self, title = '', link = '', desc = ''):
        self.__title = title
        self.__link = link
        self.__desc = desc

    @property
    def title(self):
        return self.__title

    @property
    def link(self):
        return self.__link

    @property
    def desc(self):
        return self.__desc
