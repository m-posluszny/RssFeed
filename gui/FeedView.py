from PySide2.QtGui import QStandardItem, QStandardItemModel, QColor
from PySide2.QtWidgets import QListView
import time


class FeedView(QListView):
    def __init__(self, parent=None):
        "Center view containg all articles in shorter form"
        super(FeedView, self).__init__(parent)
        self.__model = QStandardItemModel(self)
        self.setModel(self.__model)
        self.setWordWrap(True)

    def clear_list(self):
        """
        Clears article list to be able to populate it with new data
        """
        oldState = self.selectionModel().blockSignals(True)
        self.__model.clear()
        self.selectionModel().blockSignals(oldState)

    def append_message(self, site, title, desc, date, link, seen):
        """Append article to feed

        Args:
            site (string): site name
            title (string): title
            desc (string): article description
            date (string): publishing date
            link (string): link to article
            seen (bool): does user already view it?
        """
        today = time.gmtime()

        if (date.tm_year == today.tm_year) and (date.tm_yday == today.tm_yday):
            row_date = "{:02d}:{:02d}".format(date.tm_hour, date.tm_min)
        else:
            row_date = "{:02d}.{:02d}.{:02d}".format(
                date.tm_mday, date.tm_mon, date.tm_year)
        text = f"{title}   {site}\n{row_date}"
        new_item = QStandardItem(text)
        new_item.setCheckable(False)
        new_item.setEditable(False)
        new_item.setSelectable(True)
        new_item.article_bundle = {
            "site": site,
            "link": link,
            "title": title,
            "article": desc
        }
        self._og_bg = new_item.background()
        self.set_seen(new_item, seen)
        self.__model.insertRow(0, new_item)

    def set_seen(self, item, seen):
        """
        Sets seen in gui for selected row

        Args:
            item (QItem): Item corresponding to selected row
            seen (Bool): True or False
        """
        if not seen:
            item.setBackground(QColor(112, 112, 112))
        else:
            item.setBackground(self._og_bg)
