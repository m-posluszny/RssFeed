from gui.FeedView import FeedView
from gui.GroupView import GroupView
from gui.ArticleBox import ArticleBox
from PySide2.QtCore import QItemSelectionModel
from libs.urlhandler import URLHandler
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler
import dateutil.parser as DP
from PySide2.QtWidgets import (
    QSplitter,
    QVBoxLayout,
    QWidget
    
)

class MainView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.selected_group = None
        self.group_view = GroupView(self)
        self.feed_view = FeedView(self)
        self.article_box = ArticleBox(self)
        self.feed_view.selectionModel().selectionChanged.connect(self.set_article)
        self.group_view.itemClicked.connect(lambda:self.refresh_feed(self.group_view.selectedItems()[0]))
        self.refresh_groups()
        all_group = self.group_view.groups["All"]
        all_group.setExpanded(True)
        self.refresh_feed(self.group_view.groups["All"])
        self.__split = QSplitter(parent=self)
        self.__split.addWidget(self.group_view)
        self.__split.addWidget(self.feed_view)
        self.__split.addWidget(self.article_box)
        self.__split.setHandleWidth(4)
        self.__main_layout = QVBoxLayout()
        self.__main_layout.addWidget(self.__split)    
        self.setLayout(self.__main_layout)
    
    def get_user_groups(self,update=False):
        group_dict = self.entry["groups"]
        active_exists = False
        popular_name = URLHandler.popular_name
        self.group_view.clear()
        if popular_name in group_dict:
            print(group_dict[popular_name])
            self.get_single_group(group_dict,popular_name)
            group_dict.pop(popular_name)
        for group in group_dict:
            active_exists = self.get_single_group(group_dict,group)
        ix = self.group_view.model().index(0, 0)
        if not active_exists:
            self.group_view.selectionModel().setCurrentIndex(ix,QItemSelectionModel.SelectCurrent)
    
    def get_single_group(self,group_dict,group):
        active_exists = False
        indexes = group_dict[group]
        urls = []
        if self.selected_group == group:
            active_exists = True
        for index in indexes:
            print(self.entry['urls'][index]["actual_url"])
            urls.append(self.entry['urls'][index]["actual_url"])
        self.group_view.add_group(group,urls,indexes)
        return active_exists
    
    def set_group(self,item,update=False):
        if (self.selected_group != item.text(0) or update):
            self.feed_view.clear_list()
            self.selected_group = item.text(0)
            art_list=[]
            if item.rss_type == "group":
                for url_name in self.group_view.urls:
                    if item.text(0) in url_name:
                        sub_item = self.group_view.urls[url_name]
                        url = self.entry['urls'][sub_item.url_index]
                        art_list.extend(self.get_gui_articles(url))
            elif item.rss_type == "url":
                url = self.entry['urls'][item.url_index]
                art_list.extend(self.get_gui_articles(url))
            art_list = sorted(art_list, key = lambda x: (not x["seen"], x["date"]))
            for article in art_list:
                self.feed_view.append_message(**article)
    
    def get_gui_articles(self,url):
        site = url["rss_title"]
        art_list=[]
        for article in url["articles"]:
            article_bundle={
                "date" : article["pub_date_parsed"],
                "title" : article["title"],
                "desc" : article["desc"],
                "seen" : article["seen"],
                "link" : article["link"],
                "site" : site,
            }
            art_list.append(article_bundle)
        return art_list
    
    def set_article(self, current):
        row = [qmi.row() for qmi in self.feed_view.selectedIndexes()][0]
        item = self.feed_view.model().item(row)
        self.article_box.set_data(**item.article_bundle)
        self.feed_view.set_seen(item,True)

        URLHandler.setArticleSeen(item.article_bundle['link'], True)
    
    def refresh_groups(self):
        dbh = DatabaseHandler()
        self.entry = dbh.getEntry(CredentialsHandler.lastUsername)
        self.get_user_groups(update=True)
    
    def refresh_feed(self,item):
        dbh = DatabaseHandler()
        self.entry = dbh.getEntry(CredentialsHandler.lastUsername) 
        self.set_group(item,True)
