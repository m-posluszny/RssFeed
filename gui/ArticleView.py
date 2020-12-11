from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QLabel, QPushButton, QHBoxLayout, QVBoxLayout,QFrame)
from PySide2.QtCore import Qt


class ArticleView(QFrame):
    
    def __init__(self,site,link,title,article,parent=None):
        super(ArticleView,self).__init__(parent=parent)
        self.setStyleSheet("QFrame{border: 1px solid white; border-radius: 10px;} QLabel{border: 0px solid black;} QTextEdit{border: 0px solid black;} ")
        self.__layout = QVBoxLayout(self) 
        __label_font = QFont()
        __label_font.setPointSize(20)
        __text_font = QFont()
        __text_font.setPointSize(12)
        __site_font = QFont()
        __site_font.setPointSize(10)
        self.__layout.setSpacing(10)
        self.__site = QLabel(site,self)
        self.__site.setWordWrap(True)
        self.__site.setFont(__site_font)
        self.__label = QLabel(title,self)
        self.__label.setWordWrap(True)
        self.__label.setFont(__label_font)
        self.__content_box= QLabel(article,self)
        self.__content_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.__content_box.setFont(__text_font)
        self.__content_box.setWordWrap(True)
        self.__link_btn = QPushButton(f"Read more on {link}")
        self.__link_btn.setFlat(True)
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__site)
        self.__layout.addWidget(self.__content_box)
        self.__layout.addWidget(self.__link_btn)
        self.setLayout(self.__layout)