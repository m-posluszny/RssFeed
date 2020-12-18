from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction
from libs.rsshandler import RSSHandler
from libs.urlhandler import URLHandler
from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler

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
            rssh.fetchFromURL(url)
            if rssh.fetchIsSuccess():
                rssh.parseXML()

            art = rssh.returnArticles()
            URLHandler.appendDownloadedArticles(url, art)
            self.parent().parent().parent().refresh_feed()
            
        elif self.right_clicked_item.rss_type == 'group':
            groupName = self.right_clicked_item.text(0)
            dbh = DatabaseHandler()
            res = dbh.getEntry(CredentialsHandler.lastUsername)

            for idx in res['groups'][groupName]:
                url = res['urls'][idx]['actual_url']

                rssh = RSSHandler()
                rssh.fetchFromURL(url)
                if rssh.fetchIsSuccess():
                    rssh.parseXML()

                art = rssh.returnArticles()
                URLHandler.appendDownloadedArticles(url, art)

            # TODO(mateusz): Michał fix this refresh because it doesn't target any one QTreeWidgetItem
            # but the root so it falls on it's face 
            #self.parent().parent().parent().refresh_feed()
