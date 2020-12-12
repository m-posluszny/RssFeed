from PySide2 import QtWidgets
from PySide2.QtCore import QItemSelectionModel
from gui.FormView import LoginView, RegisterView
from gui.FeedView import FeedView
from gui.GroupView import GroupView
from gui.ArticleBox import ArticleBox
from gui.ListerView import ListerView
from libs.urlhandler import URLHandler
from libs.grouphandler import GroupHandler
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler
from PySide2.QtCore import QItemSelectionModel
from PySide2.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QAction,
    QInputDialog,
    QTabWidget,
    QTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget
    
)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RSS Feed")
        self.setGeometry(300, 300, 850, 500)
        self.setMinimumSize(850,500)
        self.center()
        self.__toolBar = self.menuBar()
        self.loadMenubar()
        self.showLogin()
        self.show()

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def showLogin(self):
        self.__toolBar.setVisible(False)
        self._login_view = LoginView(self)
        self.setCentralWidget(self._login_view)

    def showRegister(self):
        self.__toolBar.setVisible(False)
        self._register_view = RegisterView(self)
        self.setCentralWidget(self._register_view)

    def showFeedView(self, user_data):
        self.__toolBar.setVisible(True)
        self.mainView = QWidget()
        self.group_view = GroupView()
        self.feed_view = FeedView()
        self.article_box = ArticleBox()
        self.feed_view.selectionModel().selectionChanged.connect(self.set_article)
        self.group_view.itemDoubleClicked.connect(self.set_group)
        dbh = DatabaseHandler()
        self.entry = dbh.getEntry(CredentialsHandler.lastUsername) #
        print(self.entry)
        self.get_user_groups()
        self.__left_split = QSplitter()
        self.__right_split = QSplitter()
        self.__left_split.addWidget(self.group_view)
        self.__left_split.addWidget(self.feed_view)
        self.__left_split.setHandleWidth(4)
        self.__right_split.addWidget(self.__left_split)
        self.__right_split.addWidget(self.article_box)
        self.__right_split.setHandleWidth(4)
        self.__main_layout = QVBoxLayout()
        self.__main_layout.addWidget(self.__right_split)
        self.mainView.setLayout(self.__main_layout)
        self.setCentralWidget(self.mainView)
        
    def get_user_groups(self):
        group_dict = self.entry["groups"]
        for group in group_dict:
            indexes = group_dict[group]
            urls = []
            for index in indexes:
                urls.append(self.entry['urls'][index]["actual_url"])
            self.group_view.add_group(group,urls,indexes)
        ix = self.group_view.model().index(0, 0)
        self.group_view.selectionModel().setCurrentIndex(ix,QItemSelectionModel.SelectCurrent)
        
                
    def set_group(self,item):
        if item.rss_type == "group":
            for index in item.url_indexes:
                url = self.entry['urls'][index]
                site = url["rss_title"]
                for article in url["articles"]:
                    date = article["pub_date"]
                    title = article["title"]
                    desc = article["desc"]
                    seen = article["seen"]
                    link = article["link"]
                    self.feed_view.append_message(site,title,desc,date,link,seen)
        ix = self.feed_view.model().index(0, 0)
        self.feed_view.selectionModel().setCurrentIndex(ix,QItemSelectionModel.SelectCurrent)

    def set_article(self,current):
        row = row = [qmi.row() for qmi in self.feed_view.selectedIndexes()][0]
        item = self.feed_view.model().item(row)
        self.article_box.set_data(**item.article_bundle)

    def loadMenubar(self):
        bar = self.__toolBar
        bar.setVisible(True)
        user = bar.addMenu("App")

        addURLAction = QAction("Add URL", self)
        addURLAction.triggered.connect(self.addURLCallback)

        removeURLAction = QAction("Remove URL", self)
        removeURLAction.triggered.connect(self.removeURLCallback)
        bar.addAction(addURLAction)
        bar.addAction(removeURLAction)
    
        addGroupAction = QAction("Add Group", self)
        addGroupAction.triggered.connect(self.addGroupCallback)

        removeGroupAction = QAction("Remove Group", self)
        removeGroupAction.triggered.connect(self.removeGroupCallback)
        
        bar.addAction(addGroupAction)
        bar.addAction(removeGroupAction)
        
        addUrlGroupAction = QAction("Add URL to Group", self)
#        addUrlGroupAction.triggered.connect(self.addGroupCallback)

        removeUrlGroupAction = QAction("Remove URL from Group", self)
#        removeUrlGroupAction.triggered.connect(self.removeGroupCallback)

        bar.addAction(addUrlGroupAction)
        bar.addAction(removeUrlGroupAction)
    
        exitAction = QAction("Quit", self)
        exitAction.setShortcut("Ctrl-X")
        exitAction.triggered.connect(self.exit_app)

        logoutAction = QAction("Logout", self)
        logoutAction.triggered.connect(self.logoutCallback)
        
        user.addAction(exitAction)
        user.addAction(logoutAction)

   
    # TODO Move all menubar things to class MenuBar in gui
    def addURLCallback(self):
        res, ok = QInputDialog.getText(self, "Add URL", "Paste URL: ")

        if ok:
            urlh = URLHandler()
            if urlh.stringIsURL(res):
                URLHandler.addURL(res)
            else:
                print('it\'s not a url')


    def removeURLCallback(self):
        prompt = 'List of URLs'
        title = 'Choose URL to remove'

        db = DatabaseHandler()
        entries = db.getEntry(CredentialsHandler.lastUsername)
        data = [url['actual_url'] for url in entries['urls']]
        ls = ListerView(prompt, title, data, self)

        if ls.exec_():
            reslist = ls.getResults()
            for res in reslist:
                URLHandler.removeURL(res)

    def addGroupCallback(self):
        res, ok = QInputDialog.getText(self, "Group URL", "Enter group name: ")

        if ok:
            GroupHandler.addGroup(res)

    def removeGroupCallback(self):
        prompt = 'List of Groups'
        title = 'Choose group to remove'

        db = DatabaseHandler()
        entries = db.getEntry(CredentialsHandler.lastUsername)
        data = [url for url in entries['groups']]
        ls = ListerView(prompt, title, data, self)

        if ls.exec_():
            reslist = ls.getResults()
            for res in reslist:
                GroupHandler.removeGroup(res)
            
    def logoutCallback(self):
        self.showLogin()

    def viewAllCallback(self):
        print("This action is yet to be implemented")

    def viewGroupCallback(self,title):

        article_view = FeedView(title,self)
        

        for article in entry['urls'][0]['articles']:
            article_view.append_message()

        self._tab.addTab(article_view,title)

    def viewPopularCallback(self):
        print("This action is yet to be implemented")

    def exit_app(self):
        self.close()
