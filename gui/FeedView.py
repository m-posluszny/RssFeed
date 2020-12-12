from PySide2.QtCore import Qt 
from PySide2.QtGui import QStandardItem, QStandardItemModel, QColor
from PySide2.QtWidgets import QSizePolicy,QLabel, QListView, QVBoxLayout, QFrame, QTabWidget
from gui.ArticleBox import ArticleBox

class FeedView(QListView):
    def __init__(self, parent=None):
        super(FeedView, self).__init__(parent)
        self.__model = QStandardItemModel(self)
        self.setModel(self.__model)


    def append_message(self,site,title,desc,date,link,seen):
        text = site+title+date
        new_item = QStandardItem(text)
        new_item.setCheckable(False)
        new_item.setEditable(False)
        new_item.setSelectable(True)
        new_item.article_bundle={
            "site":site,
            "link":link,
            "title":title,
            "article":desc
        }
        self._og_bg = new_item.background();
        self.set_seen(new_item,seen)
        self.__model.appendRow(new_item)
    
    def set_seen(self,item,seen):
        if seen:
            item.setBackground(QColor(112, 112, 112))
        else:
            item.setBackground(self._og_bg)
        
