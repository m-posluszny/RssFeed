from PySide2.QtGui import QFont
from PySide2.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QFrame, QSizePolicy)
from PySide2.QtCore import Qt
from PySide2.QtWebEngineWidgets import QWebEngineView
import webbrowser


class ArticleBox(QFrame):

    def __init__(self, parent=None):
        """
        Constructor of ArticleBox which display all content of article

        Args:
            parent (QWidget): GUI parent of widget. Defaults to None.
        """
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
        self.__link_btn.clicked.connect(self.open_link)
        self.__link = ""
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__site)
        self.__layout.addWidget(self.__content_box)
        self.__layout.addWidget(self.__link_btn, alignment=Qt.AlignCenter)
        self.setLayout(self.__layout)

    def load_started_callback(self):
        """
        Method which was used to measure loading time it is executed at beginning of loading content
        """
        pass

    def load_finished_callback(self):
        """
        Method which was used to measure loading time it is executed at the end of loading content
        """
        self.__content_box.setVisible(True)

    def set_data(self, site, link, title, article):
        """
        Sets content data to data from args

        Args:
            site (string): site name
            link (string): url of the whole article
            title (string): title of the article
            article (string): content of article
        """
        self.__content_box.setHtml(article, link)
        self.__link_btn.setText(f"Read more")
        self.__link = link
        self.__site.setText(site)
        self.__label.setText(title)

    def open_link(self):
        """
        Opens article link in external browser
        """
        webbrowser.open_new_tab(self.__link)
