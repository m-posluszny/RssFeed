from PySide2.QtGui import QStandardItem, QStandardItemModel, QColor
from PySide2.QtWidgets import QListView
from PySide2.QtCore import QItemSelectionModel
from datetime import datetime

class FeedView(QListView):
    def __init__(self, parent=None):
        super(FeedView, self).__init__(parent)
        self.__model = QStandardItemModel(self)
        self.setModel(self.__model)
        self.setWordWrap(True)

    def clear_list(self):
        oldState = self.selectionModel().blockSignals(True)
        self.__model.clear()
        self.selectionModel().blockSignals(oldState)

    def append_message(self,site,title,desc,date,link,seen):
        if date.date() >= datetime.today().date():
            row_date = date.strftime("%H:%M")
        else:
            row_date = date.strftime("%d %b, %Y")
        text = f"{title}   {site}\n{row_date}"
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
        self.__model.insertRow(0,new_item)
    
    def set_seen(self,item,seen):
        if not seen:
            item.setBackground(QColor(112, 112, 112))
        else:
            item.setBackground(self._og_bg)
        
