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
        self.group_view.itemClicked.connect(self.refresh_feed)
        self.refresh_groups()
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
        self.group_view.clear()
        for group in group_dict:
            indexes = group_dict[group]
            urls = []
            if self.selected_group == group:
                active_exists = True
            for index in indexes:
                urls.append(self.entry['urls'][index]["actual_url"])
            self.group_view.add_group(group,urls,indexes)
        ix = self.group_view.model().index(0, 0)
        if not active_exists:
            self.group_view.selectionModel().setCurrentIndex(ix,QItemSelectionModel.SelectCurrent)

        # NOTE(mateusz): I'm gonna put this into the pile of code that says "WHY DO WE NEED THIS?"
        '''
        try:
            item = self.group_view.selectedItems()[0]
            self.set_group(item,update)
        except Exception as e:
            print(e)
        '''
            
    def set_group(self,item,update=False):
        if (self.selected_group != item.text(0) or update):
            self.feed_view.clear_list()
            self.selected_group = item.text(0)
            art_list=[]
            if item.rss_type == "group":
                # NOTE(mateusz): We don't always have the newst data about the articles so here we kinda have to go
                # and ask the database again for this
                for index in item.url_indexes:
                    url = self.entry['urls'][index]
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
    
    def refresh_feed(self):
        dbh = DatabaseHandler()
        # TODO(mateusz): Ask Michał if this has to be this way, in that I mean does it have to be .parent() for the selected item
#        item = self.group_view.selectedItems()[0].parent()
        item = self.group_view.selectedItems()[0]
        self.entry = dbh.getEntry(CredentialsHandler.lastUsername) 
        self.set_group(item,True)
