from gui.MainView import MainView
from PySide2 import QtWidgets
from PySide2.QtCore import QItemSelectionModel
from gui.FormView import LoginView, RegisterView
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

    def showFeedView(self):
        self.__toolBar.setVisible(True)
        self.mainView = MainView()
        self.setCentralWidget(self.mainView)
        
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
                URLHandler.addURLToGroup(res, 'All')
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
