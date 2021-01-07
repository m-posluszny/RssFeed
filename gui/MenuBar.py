from gui.ListerView import ListerView
from libs.urlhandler import URLHandler
from libs.grouphandler import GroupHandler
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QAction,
    QInputDialog,
    QAction,
    QDialog,
    QInputDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

class MenuBar:
    
    def __init__(self,menuBar,parent=None):
        self.bar = menuBar
        self.mainView = None
        self.parent = parent
        user = self.bar.addMenu("App")
        self.hideBar()
        addURLAction = QAction("Add URL", parent)
        addURLAction.triggered.connect(self.addURLCallback)

        removeURLAction = QAction("Remove URL", parent)
        removeURLAction.triggered.connect(self.removeURLCallback)
        self.bar.addAction(addURLAction)
        self.bar.addAction(removeURLAction)
    
        addGroupAction = QAction("Add Group", parent)
        addGroupAction.triggered.connect(self.addGroupCallback)

        removeGroupAction = QAction("Remove Group", parent)
        removeGroupAction.triggered.connect(self.removeGroupCallback)
        
        self.bar.addAction(addGroupAction)
        self.bar.addAction(removeGroupAction)
        
        addUrlGroupAction = QAction("Add URL to Group", parent)
        addUrlGroupAction.triggered.connect(self.addURLToGroupCallback)

        removeUrlGroupAction = QAction("Remove URL from Group", parent)
        removeUrlGroupAction.triggered.connect(self.removeURLFromGroupCallback)

        self.bar.addAction(addUrlGroupAction)
        self.bar.addAction(removeUrlGroupAction)
        
        showPopularAction = QAction("Show Popular URLs", parent)
        showPopularAction.triggered.connect(self.showPopularCallback)
        
        self.bar.addAction(showPopularAction)
        exitAction = QAction("Quit", parent)
        exitAction.setShortcut("Ctrl-X")
        exitAction.triggered.connect(self.parent.exit_app)
    
        logoutAction = QAction("Logout", parent)
        logoutAction.triggered.connect(self.logoutCallback)
        user.addAction(exitAction)
        user.addAction(logoutAction)
    
    def setMainView(self,view):
        self.mainView = view
    
    def showBar(self):
        self.bar.setVisible(True)
    
    def hideBar(self):
        self.bar.setVisible(False)
            
    def showPopularCallback(self):
        URLHandler.getMostPopularURLs()
        self.mainView.refreshGroups()
    
    def addURLCallback(self):
        res, ok = QInputDialog.getText(self.parent, "Add URL", "Paste URL: ")

        if ok:
            if URLHandler.stringIsURL(res):
                URLHandler.addURL(res)
                index = URLHandler.addURLToGroup(res, 'All')
                self.mainView.group_view.addUrl(res,'All',index)
            else:
                print('it\'s not a url')
    
    def removeURLCallback(self):
        prompt = 'List of URLs'
        title = 'Choose URL to remove'

        db = DatabaseHandler()
        entries = db.getEntry(CredentialsHandler.lastUsername)
        data = [url['actual_url'] for url in entries['urls']]
        ls = ListerView(prompt, title, data, self.parent)
        ls.enableButtonBox()

        if ls.exec_():
            reslist = ls.getResults()
            for res in reslist:
                URLHandler.removeURL(res)
                self.mainView.group_view.removeUrl(res,"All")

    def addGroupCallback(self):
        res, ok = QInputDialog.getText(self.parent, "Group URL", "Enter group name: ")
        if ok:
            GroupHandler.addGroup(res)
            self.mainView.group_view.addGroup(res,[],[])
             
            
    def removeGroupCallback(self):
        prompt = 'List of Groups'
        title = 'Choose group to remove'

        db = DatabaseHandler()
        entries = db.getEntry(CredentialsHandler.lastUsername)
        data = [url for url in entries['groups']]
        ls = ListerView(prompt, title, data, self.parent)
        ls.enableButtonBox()

        if ls.exec_():
            reslist = ls.getResults()
            for res in reslist:
                GroupHandler.removeGroup(res)
                self.mainView.group_view.removeGroup(res)
                
    def addURLToGroupCallback(self):
        w = QWidget()
        f = QHBoxLayout(w)

        db = DatabaseHandler()
        entries = db.getEntry(CredentialsHandler.lastUsername)

        ldata = [url for url in entries['groups']]
        ls = ListerView('Groups', 'Groups', ldata, self.parent)

        rdata = [url['actual_url'] for url in entries['urls']]
        rs = ListerView('Urls', 'Urls', rdata, self.parent)

        rs.layout().setContentsMargins(0,0,0,0)
        ls.layout().setContentsMargins(0,0,0,0)
        f.addWidget(ls)
        f.addWidget(rs)

        q = QDialog(self.parent)
        q.setWindowTitle('Add URL to Group')
        mf = QVBoxLayout(q)
        mf.addWidget(w)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self.parent)
        mf.addWidget(buttonBox)
        buttonBox.accepted.connect(q.accept)
        buttonBox.rejected.connect(q.reject)

        if q.exec_():
            groups = ls.getResults()
            urls = rs.getResults()

            for group in groups:
                for url in urls:
                    index = URLHandler.addURLToGroup(url, group)
                    self.mainView.group_view.addUrl(url,group,index)

    def removeURLFromGroupCallback(self):
        w = QWidget()
        f = QHBoxLayout(w)

        db = DatabaseHandler()
        entries = db.getEntry(CredentialsHandler.lastUsername)

        ldata = [url for url in entries['groups']]
        ls = ListerView('Groups', 'Groups', ldata, self.parent)

        rdata = [url['actual_url'] for url in entries['urls']]
        rs = ListerView('Urls', 'Urls', rdata, self.parent)

        rs.layout().setContentsMargins(0,0,0,0)
        ls.layout().setContentsMargins(0,0,0,0)
        f.addWidget(ls)
        f.addWidget(rs)

        q = QDialog(self.parent)
        q.setWindowTitle('Remove URL from Group')
        mf = QVBoxLayout(q)
        mf.addWidget(w)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self.parent)
        mf.addWidget(buttonBox)
        buttonBox.accepted.connect(q.accept)
        buttonBox.rejected.connect(q.reject)

        if q.exec_():
            groups = ls.getResults()
            urls = rs.getResults()

            for group in groups:
                for url in urls:
                    URLHandler.removeURLFromGroup(url, group)
                    self.mainView.group_view.removeUrl(url,group)
                    
    def logoutCallback(self):
        self.parent.showLogin()
