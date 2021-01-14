class RSSHeader:
    def __init__(self, title='', link='', desc=''):
        """
        Constructor containg data of rss header

        Args:
            title (str, optional): Article title. Defaults to ''.
            link (str, optional): Article link. Defaults to ''.
            desc (str, optional): Article description. Defaults to ''.
        """
        self.__title = title
        self.__link = link
        self.__desc = desc

    """
    Getters which returns title, link, and description of this object

    """
    @property
    def title(self):
        return self.__title

    @property
    def link(self):
        return self.__link

    @property
    def desc(self):
        return self.__desc
