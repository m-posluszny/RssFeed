import PySide2
from PySide2 import QtWidgets
from PySide2.QtGui import QFont, QImage, QPixmap
from PySide2.QtWidgets import (QLabel, QPushButton, QVBoxLayout,QFrame,QSizePolicy)
from PySide2.QtCore import QSize, Qt, QEvent
import re
import urllib.request
        
class ImageWidget(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)

    def hasHeightForWidth(self):
        return self.pixmap() is not None

    def heightForWidth(self, w):
        if self.pixmap():
            return int(w * (self.pixmap().height() / self.pixmap().width()))
        
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
        self.__layout.setAlignment(Qt.AlignTop)
        self.__site = QLabel(site,self)
        self.__site.setWordWrap(True)
        self.__site.setFont(__site_font)
        self.__label = QLabel(title,self)
        self.__label.setWordWrap(True)
        self.__label.setFont(__label_font)
        self.__label_img = None
        self.__content_box= QLabel(self)
        self.__content_box.setTextFormat(Qt.RichText)
        reg_url = re.compile(r'(<img.*src="(.*?)".*?>)')
        img_urls = reg_url.findall(article)    
        if len(img_urls) > 0:
            img_urls = img_urls[0]
        if len(img_urls) > 1:
            img_tag = img_urls[0]
            img_url = img_urls[1]
            article = article.replace(img_tag,'')
            data = urllib.request.urlopen(img_url).read()
            image = QImage()
            image.loadFromData(data)
            aspect = image.height()/image.width()
            pixmap = QPixmap(image)
            self.__label_img = ImageWidget(parent=self)
            pixmap= pixmap.scaledToWidth(510)
            self.__label_img.setPixmap(pixmap)
            self.__label_img.setAlignment(Qt.AlignCenter)
            self.__label_img.setScaledContents(False)
        self.__content_box.setText(article)
        self.__content_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.__content_box.setFont(__text_font)
        self.__content_box.setWordWrap(True)
        self.__link_btn = QPushButton(f"Read more on {link}")
        self.__link_btn.setFlat(True)
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__site)
        self.__layout.addWidget(self.__content_box)
        if self.__label_img:
            self.__layout.addWidget(self.__label_img)
        self.__layout.addWidget(self.__link_btn, alignment=Qt.AlignCenter)
        self.setLayout(self.__layout)
    