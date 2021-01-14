from gui.FeedView import FeedView
from gui.GroupView import GroupView
from gui.ArticleBox import ArticleBox
from PySide2.QtCore import QItemSelectionModel
from libs.urlhandler import URLHandler
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler
from PySide2.QtWidgets import QSplitter, QHBoxLayout, QWidget


class MainView(QWidget):

    def __init__(self):
        """
        MainView of the application, contains three Widgets divided by splitters
        from the left:
        GroupView containg all groups info
        FeedView containg all feed
        ArticleBox containg selected article and its content
        """
        super().__init__()
        self.selected_group = None
        self.group_view = GroupView(self)
        self.feed_view = FeedView(self)
        self.article_box = ArticleBox(self)
        self.feed_view.selectionModel().selectionChanged.connect(self.set_article)
        self.group_view.itemClicked.connect(
            lambda: self.refresh_feed(self.group_view.selectedItems()[0]))
        self.refresh_groups()
        all_group = self.group_view.groups["All"]
        all_group.setExpanded(True)
        self.refresh_feed(self.group_view.groups["All"])
        self.__split = QSplitter(parent=self)
        self.__split.addWidget(self.group_view)
        self.__split.addWidget(self.feed_view)
        self.__split.addWidget(self.article_box)
        self.__split.setHandleWidth(4)
        self.__main_layout = QHBoxLayout()
        self.__main_layout.addWidget(self.__split)
        self.setLayout(self.__main_layout)

    def get_user_groups(self, update=False):
        """
        Load all user groups from database to gui

        Args:
            update (bool, optional): Enforces selecting group to the first group, Defaults to False.
        """
        group_dict = self.entry["groups"]
        active_exists = False
        popular_name = URLHandler.popular_name
        self.group_view.clear()
        if popular_name in group_dict:
            self.get_single_group(group_dict, popular_name)
            group_dict.pop(popular_name)
        for group in group_dict:
            active_exists = self.get_single_group(group_dict, group)
        ix = self.group_view.model().index(0, 0)
        if not active_exists or update:
            self.group_view.selectionModel().setCurrentIndex(
                ix, QItemSelectionModel.SelectCurrent)
            self.group_view.expand(ix)

    def get_single_group(self, group_dict, group):
        """
        Add single group to group view, returns active groups

        Args:
            group_dict (dict): dictionary of user groups from database
            group (string): group name

        Returns:
            bool: true if selected group is the group that is being added
        """
        active_exists = False
        indexes = group_dict[group]
        urls = []
        if self.selected_group == group:
            active_exists = True
        for index in indexes:
            urls.append(self.entry['urls'][index]["actual_url"])
        self.group_view.add_group(group, urls, indexes)
        return active_exists

    def set_group(self, item, update=False):
        """
        Sets group to provided in item arg
        If update is set to True group will update even if it is not currenlt selected,
        used for refreshing

        Args:
            item (QItem): selected group 
            update (bool, optional): Enforces group update, Defaults to False.
        """
        if (self.selected_group != item.text(0) or update):
            self.feed_view.clear_list()
            self.selected_group = item.text(0)
            art_list = []
            if item.rss_type == "group":
                for url_name in self.group_view.urls:
                    if item.text(0) in url_name:
                        sub_item = self.group_view.urls[url_name]
                        url = self.entry['urls'][sub_item.url_index]
                        art_list.extend(self.get_gui_articles(url))
            elif item.rss_type == "url":
                url = self.entry['urls'][item.url_index]
                art_list.extend(self.get_gui_articles(url))
            art_list = sorted(art_list, key=lambda x: (
                not x["seen"], x["date"]))
            for article in art_list:
                self.feed_view.append_message(**article)

    def get_gui_articles(self, url):
        """
        Returns all articles from selected url

        Args:
            url (string): url

        Returns:
            list: list of article objects
        """
        site = url["rss_title"]
        art_list = []
        for article in url["articles"]:
            article_bundle = {
                "date": article["pub_date_parsed"],
                "title": article["title"],
                "desc": article["desc"],
                "seen": article["seen"],
                "link": article["link"],
                "site": site,
            }
            art_list.append(article_bundle)
        return art_list

    def set_article(self, current):
        """
        Sets selected article to seen and updates data of articlebox
        to view newest content

        Args:
            current (QItem): item conteining row with selected article
        """
        row = [qmi.row() for qmi in self.feed_view.selectedIndexes()][0]
        item = self.feed_view.model().item(row)
        self.article_box.set_data(**item.article_bundle)
        self.feed_view.set_seen(item, True)

        URLHandler.set_article_seen(item.article_bundle['link'], True)

    def refresh_groups(self, download=False):
        """
        Refreshes groups after adding/removing group or url

        Args:
            download (bool, optional): Option to fetch newset article while refreshing content. Defaults to False.
        """
        dbh = DatabaseHandler()
        self.entry = dbh.get_entry(CredentialsHandler.lastUsername)
        self.get_user_groups(update=True)
        if download:
            self.group_view.menu_refresh_callback(
                self.group_view.selectedItems()[0])

    def refresh_feed(self, item):
        """Refreshes content of FeedView

        Args:
            item (QItem): Item of selected group from groupview
        """
        dbh = DatabaseHandler()
        self.entry = dbh.get_entry(CredentialsHandler.lastUsername)
        self.set_group(item, True)
