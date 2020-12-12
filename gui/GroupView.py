from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction
from libs.rsshandler import RSSHandler
from libs.urlhandler import URLHandler

class GroupView(QTreeWidget):
    
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def add_group(self,group_name,urls,indexes):
        group_tree =  QTreeWidgetItem([group_name])
        group_tree.rss_type = "group"
        for url in urls:
            url_row = QTreeWidgetItem([url])
            url_row.rss_type = "url"
            group_tree.addChild(url_row)
        group_tree.url_indexes = indexes
        self.addTopLevelItem(group_tree)
    
    def showContextMenu(self, pos):
        item = self.itemAt(pos)
        assert(item.columnCount() >= 1)
        self.right_clicked_item = item

        menu = QMenu()
        menu.addAction(QAction('Refresh', self, triggered=self.menuRefreshCallback))
        menu.exec_(QCursor.pos())

    def menuRefreshCallback(self):
        if self.right_clicked_item.rss_type == 'url':
            url = self.right_clicked_item.text(0)

            rssh = RSSHandler()
            rssh.retriveDataFromURL(url)
            rssh.parseXML()

            art = rssh.returnArticles()
            URLHandler.appendDownloadedArticles(url, art)
        elif self.right_clicked_item.rss_type == 'group':
            print('Group refresh is not yet implemented')
