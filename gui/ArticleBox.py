from PySide2.QtGui import QFont
from PySide2.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QFrame, QSizePolicy)
from PySide2.QtCore import Qt
from PySide2.QtWebEngineWidgets import QWebEngineView
import webbrowser


class ArticleBox(QFrame):

    def __init__(self, parent=None):
        super(ArticleBox, self).__init__(parent=parent)
        self.setStyleSheet(
            "QFrame{border: 1px solid white; border-radius: 10px;} QLabel{border: 0px solid black;} QTextEdit{border: 0px solid black;} ")
        self.__layout = QVBoxLayout(self)
        __label_font = QFont()
        __label_font.setPointSize(20)
        __text_font = QFont()
        __text_font.setPointSize(12)
        __site_font = QFont()
        __site_font.setPointSize(10)
        self.__layout.setSpacing(10)
        self.__layout.setAlignment(Qt.AlignTop)
        self.__site = QLabel(parent=self)
        self.__site.setWordWrap(True)
        self.__site.setFont(__site_font)
        self.__label = QLabel(parent=self)
        self.__label.setWordWrap(True)
        self.__label.setFont(__label_font)
        self.__content_box = QWebEngineView()
        self.__content_box.setVisible(False)
        self.__content_box.setMinimumSize(300, 300)
        self.__content_box.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.__content_box.loadStarted.connect(self.load_started_callback)
        self.__content_box.loadFinished.connect(self.load_finished_callback)
        self.__link_btn = QPushButton()
        self.__link_btn.setFlat(True)
        self.__link_btn.clicked.connect(self.openLink)
        self.__link = ""
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__site)
        self.__layout.addWidget(self.__content_box)
        self.__layout.addWidget(self.__link_btn, alignment=Qt.AlignCenter)
        self.setLayout(self.__layout)

    def load_started_callback(self):
        pass

    def load_finished_callback(self):
        self.__content_box.setVisible(True)

    def setData(self, site, link, title, article):
        self.__content_box.setHtml(article, link)
        self.__link_btn.setText(f"Read more")
        self.__link = link
        self.__site.setText(site)
        self.__label.setText(title)

    def openLink(self):
        webbrowser.open_new_tab(self.__link)
