class Article:
    def __init__(self, title, link, content, date):
        self.__title = title
        self.__link = link
        self.__content = content
        self.__date = date
    def __str__(self):
        return "[{}][{}][{}][{}]".format(self.__title, self.__date, self.__link, self.__content)
