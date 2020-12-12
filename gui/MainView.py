from gui.FeedView import FeedView
from gui.GroupView import GroupView
from gui.ArticleBox import ArticleBox
from PySide2.QtCore import QItemSelectionModel
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler
from PySide2.QtWidgets import (
    QSplitter,
    QVBoxLayout,
    QWidget
    
)

class MainView(QWidget):
    
    def __init__(self):
        super().__init__()
        dbh = DatabaseHandler()
        self.selected_group = None
        self.group_view = GroupView()
        self.feed_view = FeedView()
        self.article_box = ArticleBox()
        self.feed_view.selectionModel().selectionChanged.connect(self.set_article)
        self.group_view.itemDoubleClicked.connect(self.set_group)
        self.entry = dbh.getEntry(CredentialsHandler.lastUsername) #
        self.get_user_groups()
        self.__left_split = QSplitter()
        self.__right_split = QSplitter()
        self.__left_split.addWidget(self.group_view)
        self.__left_split.addWidget(self.feed_view)
        self.__left_split.setHandleWidth(4)
        self.__right_split.addWidget(self.__left_split)
        self.__right_split.addWidget(self.article_box)
        self.__right_split.setHandleWidth(4)
        self.__main_layout = QVBoxLayout()
        self.__main_layout.addWidget(self.__right_split)    
        self.setLayout(self.__main_layout)
    
    def get_user_groups(self):
        group_dict = self.entry["groups"]
        for group in group_dict:
            indexes = group_dict[group]
            urls = []
            for index in indexes:
                urls.append(self.entry['urls'][index]["actual_url"])
            self.group_view.add_group(group,urls,indexes)
        ix = self.group_view.model().index(0, 0)
        self.group_view.selectionModel().setCurrentIndex(ix,QItemSelectionModel.SelectCurrent)
        try:
            item = self.group_view.selectedItems()[0]
            self.set_group(item)
        except:
            ...
            
    def set_group(self,item):
        if item.rss_type == "group" and self.selected_group != item:
            self.feed_view.clear_list()
            self.selected_group == item
            for index in item.url_indexes:
                url = self.entry['urls'][index]
                site = url["rss_title"]
                for article in url["articles"]:
                    date = article["pub_date"]
                    title = article["title"]
                    desc = article["desc"]
                    seen = article["seen"]
                    link = article["link"]
                    self.feed_view.append_message(site,title,desc,date,link,seen)
        ix = self.feed_view.model().index(0, 0)
        self.feed_view.selectionModel().setCurrentIndex(ix,QItemSelectionModel.SelectCurrent)

    def set_article(self,current):
        try:
            row = [qmi.row() for qmi in self.feed_view.selectedIndexes()][0]
            item = self.feed_view.model().item(row)
            self.article_box.set_data(**item.article_bundle)
        except:
            pass