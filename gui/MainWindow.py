from gui.MainView import MainView
from gui.FormView import LoginView, RegisterView
from gui.ListerView import ListerView
from gui.MenuBar import MenuBar
from libs.urlhandler import URLHandler
from libs.grouphandler import GroupHandler
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler
from pyside_material import apply_stylesheet
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QAction,
    QInputDialog,
    QMainWindow,
    QAction,
    QDialog,
    QInputDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):

    def __init__(self,app):
        super(MainWindow, self).__init__()
        self.__app = app
        apply_stylesheet(app, theme='dark_amber.xml')
        self.setWindowTitle("RSS Feed")
        self.setGeometry(300, 300, 850, 500)
        self.setMinimumSize(850,500)
        self.center()
        self.__toolBar = MenuBar(self.menuBar(),self)

        debugNoLogin = False
        if debugNoLogin:
            credHandler = CredentialsHandler('admin','admin')
            credHandler.encryptCredentials()
            if credHandler.areCredValid():
                self.showFeedView()
            else:
                self.showRegister()
        else:
            self.showLogin()

        self.setIcon()
        self.show()

    def setIcon(self):
        icon = QIcon('res/icon.png')
        self.setWindowIcon(icon)

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def showLogin(self):
        self.__toolBar.hideBar()
        self._login_view = LoginView(self)
        self.setCentralWidget(self._login_view)

    def showRegister(self):
        self.__toolBar.hideBar()
        self._register_view = RegisterView(self)
        self.setCentralWidget(self._register_view)

    def showFeedView(self):
        self.__toolBar.showBar()
        self.mainView = MainView()
        self.__toolBar.setMainView(self.mainView)
        self.setCentralWidget(self.mainView)
        
    # def loadMenubar(self):
    #     bar = self.__toolBar
    #     bar.setVisible(True)
    #     user = bar.addMenu("App")

    #     addURLAction = QAction("Add URL", self)
    #     addURLAction.triggered.connect(self.addURLCallback)

    #     removeURLAction = QAction("Remove URL", self)
    #     removeURLAction.triggered.connect(self.removeURLCallback)
    #     bar.addAction(addURLAction)
    #     bar.addAction(removeURLAction)
    
    #     addGroupAction = QAction("Add Group", self)
    #     addGroupAction.triggered.connect(self.addGroupCallback)

    #     removeGroupAction = QAction("Remove Group", self)
    #     removeGroupAction.triggered.connect(self.removeGroupCallback)
        
    #     bar.addAction(addGroupAction)
    #     bar.addAction(removeGroupAction)
        
    #     addUrlGroupAction = QAction("Add URL to Group", self)
    #     addUrlGroupAction.triggered.connect(self.addURLToGroupCallback)

    #     removeUrlGroupAction = QAction("Remove URL from Group", self)
    #     removeUrlGroupAction.triggered.connect(self.removeURLFromGroupCallback)

    #     bar.addAction(addUrlGroupAction)
    #     bar.addAction(removeUrlGroupAction)
        
    #     showPopularAction = QAction("Show Popular URLs", self)
    #     showPopularAction.triggered.connect(self.showPopularCallback)
        
    #     bar.addAction(showPopularAction)
    #     #themeMenu = QMenu("Theme",self)
    #     exitAction = QAction("Quit", self)
    #     exitAction.setShortcut("Ctrl-X")
    #     exitAction.triggered.connect(self.exit_app)
    #     # for theme in list_themes():
    #     #     themeAction = QAction(theme,self)
    #     #     themeAction.triggered.connect(lambda: self.switch_theme(theme))
    #     #     themeMenu.addAction(themeAction)
    #     logoutAction = QAction("Logout", self)
    #     logoutAction.triggered.connect(self.logoutCallback)
    #     #user.addMenu(themeMenu)
    #     user.addAction(exitAction)
    #     user.addAction(logoutAction)


    # def showPopularCallback(self):
    #     urls,indexes = URLHandler.getMostPopularURLs()
    #     self.mainView.refreshGroups()
    
    # # TODO Move all menubar things to class MenuBar in gui
    # def addURLCallback(self):
    #     res, ok = QInputDialog.getText(self, "Add URL", "Paste URL: ")

    #     if ok:
    #         urlh = URLHandler()
    #         if urlh.stringIsURL(res):
    #             URLHandler.addURL(res)
    #             index = URLHandler.addURLToGroup(res, 'All')
    #             self.mainView.group_view.addUrl(res,'All',index)
    #         else:
    #             print('it\'s not a url')
    
    # def removeURLCallback(self):
    #     prompt = 'List of URLs'
    #     title = 'Choose URL to remove'

    #     db = DatabaseHandler()
    #     entries = db.getEntry(CredentialsHandler.lastUsername)
    #     data = [url['actual_url'] for url in entries['urls']]
    #     ls = ListerView(prompt, title, data, self)
    #     ls.enableButtonBox()

    #     if ls.exec_():
    #         reslist = ls.getResults()
    #         for res in reslist:
    #             URLHandler.removeURL(res)
    #             self.mainView.group_view.removeUrl(res,"All")

    # def addGroupCallback(self):
    #     res, ok = QInputDialog.getText(self, "Group URL", "Enter group name: ")
    #     if ok:
    #         GroupHandler.addGroup(res)
    #         self.mainView.group_view.addGroup(res,[],[])
             
            
    # def removeGroupCallback(self):
    #     prompt = 'List of Groups'
    #     title = 'Choose group to remove'

    #     db = DatabaseHandler()
    #     entries = db.getEntry(CredentialsHandler.lastUsername)
    #     data = [url for url in entries['groups']]
    #     ls = ListerView(prompt, title, data, self)
    #     ls.enableButtonBox()

    #     if ls.exec_():
    #         reslist = ls.getResults()
    #         for res in reslist:
    #             GroupHandler.removeGroup(res)
    #             self.mainView.group_view.removeGroup(res)
                
    # def addURLToGroupCallback(self):
    #     w = QWidget()
    #     f = QHBoxLayout(w)

    #     db = DatabaseHandler()
    #     entries = db.getEntry(CredentialsHandler.lastUsername)

    #     ldata = [url for url in entries['groups']]
    #     ls = ListerView('Groups', 'Groups', ldata, self)

    #     rdata = [url['actual_url'] for url in entries['urls']]
    #     rs = ListerView('Urls', 'Urls', rdata, self)

    #     rs.layout().setContentsMargins(0,0,0,0)
    #     ls.layout().setContentsMargins(0,0,0,0)
    #     f.addWidget(ls)
    #     f.addWidget(rs)

    #     q = QDialog(self)
    #     q.setWindowTitle('Add URL to Group')
    #     mf = QVBoxLayout(q)
    #     mf.addWidget(w)

    #     buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
    #     mf.addWidget(buttonBox)
    #     buttonBox.accepted.connect(q.accept)
    #     buttonBox.rejected.connect(q.reject)

    #     if q.exec_():
    #         groups = ls.getResults()
    #         urls = rs.getResults()

    #         for group in groups:
    #             for url in urls:
    #                 index = URLHandler.addURLToGroup(url, group)
    #                 self.mainView.group_view.addUrl(url,group,index)

    # def removeURLFromGroupCallback(self):
    #     w = QWidget()
    #     f = QHBoxLayout(w)

    #     db = DatabaseHandler()
    #     entries = db.getEntry(CredentialsHandler.lastUsername)

    #     ldata = [url for url in entries['groups']]
    #     ls = ListerView('Groups', 'Groups', ldata, self)

    #     rdata = [url['actual_url'] for url in entries['urls']]
    #     rs = ListerView('Urls', 'Urls', rdata, self)

    #     rs.layout().setContentsMargins(0,0,0,0)
    #     ls.layout().setContentsMargins(0,0,0,0)
    #     f.addWidget(ls)
    #     f.addWidget(rs)

    #     q = QDialog(self)
    #     q.setWindowTitle('Remove URL from Group')
    #     mf = QVBoxLayout(q)
    #     mf.addWidget(w)

    #     buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
    #     mf.addWidget(buttonBox)
    #     buttonBox.accepted.connect(q.accept)
    #     buttonBox.rejected.connect(q.reject)

    #     if q.exec_():
    #         groups = ls.getResults()
    #         urls = rs.getResults()

    #         for group in groups:
    #             for url in urls:
    #                 URLHandler.removeURLFromGroup(url, group)
    #                 self.mainView.group_view.removeUrl(url,group)
            
    # def logoutCallback(self):
    #     self.showLogin()

    def exit_app(self):
        self.close()
