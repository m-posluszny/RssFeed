from PySide2.QtCore import Qt 
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QSizePolicy,QLabel, QScrollArea, QVBoxLayout, QFrame, QTabWidget
from gui.ArticleView import ArticleView

class FeedView(QScrollArea):
    def __init__(self,group_name, parent=None):
        super(FeedView, self).__init__(parent)
        self.setWidgetResizable(True)
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(5, 5, 5, 5)
        self.__layout.setSpacing(10)
        self.__layout.setAlignment(Qt.AlignTop)
        __title_font = QFont()
        __title_font.setPointSize(30)
        self.__title_label = QLabel(group_name)
        self.__title_label.setFont(__title_font)
        self.__title_label.setAlignment( Qt.AlignCenter)
        self.__news_widget = QFrame()
        self.__news_widget.setLayout(self.__layout)
        self.__layout.addWidget(self.__title_label)
        self.setWidget(self.__news_widget)


    def append_message(self,site,link,title,article):
        new_item = ArticleView(site,link,title,article,self)
        new_item.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.__layout.insertWidget(self.__layout.count() , new_item)