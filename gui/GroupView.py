from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction
from libs.rsshandler import RSSHandler
from libs.urlhandler import URLHandler
from libs.databasehandler import DatabaseHandler
from libs.credhandler import CredentialsHandler


class GroupView(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.root = self.invisibleRootItem()
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.addTopLevelItem(self.root)
        self.groups = {}
        self.urls = {}

    def add_group(self, group_name, urls, indexes):
        group_tree = QTreeWidgetItem([group_name])
        group_tree.rss_type = "group"
        self.groups[group_name] = group_tree
        for url, idx in zip(urls, indexes):
            self.add_url(url, group_name, idx)
        self.addTopLevelItem(group_tree)

    def add_url(self, url, group_name, index):
        url_row = QTreeWidgetItem([url])
        url_row.rss_type = "url"
        url_row.url_index = index
        self.urls[f"{group_name}_{url}"] = url_row
        self.groups[group_name].addChild(url_row)

    def remove_group(self, group_name):
        item = self.groups[group_name]
        self.root.removeChild(item)
        self.groups.pop(group_name)
        to_rem = []
        for url_id in self.urls.keys():
            if group_name in url_id:
                to_rem.append(url_id)
        for rem in to_rem:
            self.urls.pop(rem)

    def remove_url(self, url, group_name):
        if (group_name == "All"):
            for group in self.groups.keys():
                url_id = f"{group}_{url}"
                if url_id in self.urls:
                    item = self.urls[url_id]
                    self.groups[group_name].removeChild(item)
                    self.urls.pop(url_id)
        else:
            url_id = f"{group_name}_{url}"
            if url_id in self.urls:
                item = self.urls[url_id]
                self.groups[group_name].removeChild(item)
                self.urls.pop(url_id)

    def show_context_menu(self, pos):
        item = self.itemAt(pos)
        assert(item.columnCount() >= 1)

        menu = QMenu()
        menu.addAction(
            QAction('Refresh', self, triggered=lambda: self.menu_refresh_callback(item)))
        menu.exec_(QCursor.pos())

    def menu_refresh_callback(self, clicked_item):
        if clicked_item.rss_type == 'url':
            url = clicked_item.text(0)
            self.refresh_url_data(url)
            self.parent().parent().refresh_feed(clicked_item)

        elif clicked_item.rss_type == 'group':
            groupName = clicked_item.text(0)
            dbh = DatabaseHandler()
            res = dbh.get_entry(CredentialsHandler.lastUsername)

            for idx in res['groups'][groupName]:
                self.refresh_url_data(res['urls'][idx]['actual_url'])

            self.parent().parent().refresh_feed(clicked_item)

    def refresh_url_data(self,url):
        rssh = RSSHandler()
        rssh.fetch_from_url(url)
        if rssh.fetch_is_success():
            rssh.parse_xml()

        art = rssh.return_articles()
        URLHandler.append_downloaded_articles(url, art)
