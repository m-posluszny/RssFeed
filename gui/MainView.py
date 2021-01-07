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
    QHBoxLayout,
    QWidget,
    
)

class MainView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.selected_group = None
        self.group_view = GroupView(self)
        self.feed_view = FeedView(self)
        self.article_box = ArticleBox(self)
        self.feed_view.selectionModel().selectionChanged.connect(self.setArticle)
        self.group_view.itemClicked.connect(lambda:self.refreshFeed(self.group_view.selectedItems()[0]))
        self.refreshGroups()
        all_group = self.group_view.groups["All"]
        all_group.setExpanded(True)
        self.refreshFeed(self.group_view.groups["All"])
        self.__split = QSplitter(parent=self)
        self.__split.addWidget(self.group_view)
        self.__split.addWidget(self.feed_view)
        self.__split.addWidget(self.article_box)
        self.__split.setHandleWidth(4)
        self.__main_layout = QHBoxLayout()
        self.__main_layout.addWidget(self.__split)    
        self.setLayout(self.__main_layout)
    
    def getUserGroups(self,update=False):
        group_dict = self.entry["groups"]
        active_exists = False
        popular_name = URLHandler.popular_name
        self.group_view.clear()
        if popular_name in group_dict:
#            print(group_dict[popular_name])
            self.getSingleGroup(group_dict,popular_name)
            group_dict.pop(popular_name)
        for group in group_dict:
            active_exists = self.getSingleGroup(group_dict,group)
        ix = self.group_view.model().index(0, 0)
        # NOTE(mateusz): This takes 40ms at start-up and does nothing.
        #if not active_exists:
        #    self.group_view.selectionModel().setCurrentIndex(ix,QItemSelectionModel.SelectCurrent)

        # NOTE(mateusz): I'm gonna put this into the pile of code that says "WHY DO WE NEED THIS?"
        '''
        try:
            item = self.group_view.selectedItems()[0]
            self.set_group(item,update)
        except Exception as e:
            print(e)
        '''

        # TODO(mateusz): this is to be check really because I don't know if it works or not
        if not active_exists:
            self.group_view.selectionModel().setCurrentIndex(ix,QItemSelectionModel.SelectCurrent)
    
    def getSingleGroup(self,group_dict,group):
        active_exists = False
        indexes = group_dict[group]
        urls = []
        if self.selected_group == group:
            active_exists = True
        for index in indexes:
#            print(self.entry['urls'][index]["actual_url"])
            urls.append(self.entry['urls'][index]["actual_url"])
        self.group_view.addGroup(group,urls,indexes)
        return active_exists
    
    def setGroup(self,item,update=False):
        if (self.selected_group != item.text(0) or update):
            self.feed_view.clearList()
            self.selected_group = item.text(0)
            art_list=[]
            if item.rss_type == "group":
                for url_name in self.group_view.urls:
                    if item.text(0) in url_name:
                        sub_item = self.group_view.urls[url_name]
                        url = self.entry['urls'][sub_item.url_index]
                        art_list.extend(self.getGuiArticles(url))
            elif item.rss_type == "url":
                url = self.entry['urls'][item.url_index]
                art_list.extend(self.getGuiArticles(url))
            art_list = sorted(art_list, key = lambda x: (not x["seen"], x["date"]))
            for article in art_list:
                self.feed_view.appendMessage(**article)
    
    def getGuiArticles(self,url):
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
    
    def setArticle(self, current):
        row = [qmi.row() for qmi in self.feed_view.selectedIndexes()][0]
        item = self.feed_view.model().item(row)
        self.article_box.setData(**item.article_bundle)
        self.feed_view.setSeen(item,True)

        URLHandler.setArticleSeen(item.article_bundle['link'], True)
    
    def refreshGroups(self):
        dbh = DatabaseHandler()
        self.entry = dbh.getEntry(CredentialsHandler.lastUsername)
        self.getUserGroups(update=True)
    
    def refreshFeed(self,item):
        dbh = DatabaseHandler()
        self.entry = dbh.getEntry(CredentialsHandler.lastUsername) 
        self.setGroup(item,True)
