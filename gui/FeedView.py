from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QFrame, QTabWidget
from gui.ArticleView import ArticleView

class FeedView(QScrollArea):
    def __init__(self,group_name, parent=None):
        super(FeedView, self).__init__(parent)
        self.setWidgetResizable(True)
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(5, 5, 5, 5)
        self.__layout.setSpacing(10)
        self.__layout.setAlignment(Qt.AlignTop)
        self.__layout.addStretch(1)
        __title_font = QFont()
        __title_font.setPointSize(30)
        self.__title_label = QLabel(group_name)
        self.__title_label.setFont(__title_font)
        self.__title_label.setAlignment(Qt.AlignCenter)
        self.__layout.addWidget(self.__title_label)
        self.__news_widget = QFrame()
        self.__news_widget.setLayout(self.__layout)
        self.setWidget(self.__news_widget)
        
        self.append_message("site.com","site.com/article1.html",'TITLE_ol',"ARTICLEART ICLEARTICLEARTICLEART ICLEARTICLEARTI CLEATICLEA ARTICLERTICLEAR TICLEARTICLEARTICLE")     

        self.append_message("site.com","site.com/article1.html",'TITLE_mid',"ARTICLEART ICLEARTICLEARTICLEART ICLEARTICLEARTI CLEATICLEA ARTICLERTICLEAR TICLEARTICLEARTICLE")     

        self.append_message("site.com","site.com/article1.html",'TITLE',"ARTICLEART ICLEARTICLEARTICLEART ICLEARTICLEARTI CLEATICLEA ARTICLERTICLEAR TICLEARTICLEARTICLE")     

    def append_message(self,site,link,title,article):
        new_item = ArticleView(site,link,title,article,self)
        layout = self.__news_widget.layout()
        layout.insertWidget(layout.count() , new_item)