from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem

class GroupView(QTreeWidget):
    
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setColumnCount(1)
        self.setHeaderHidden(True)

    def add_group(self,group_name,urls,indexes):
        group_tree =  QTreeWidgetItem([group_name])
        group_tree.rss_type = "group"
        for url in urls:
            url_row = QTreeWidgetItem([url])
            url_row.rss_type = "url"
            group_tree.addChild(url_row)
        group_tree.url_indexes = indexes
        self.addTopLevelItem(group_tree)
    
    