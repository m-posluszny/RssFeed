from gui.FormView import LoginView, RegisterView
from gui.MainView import MainView
from gui.ListerView import ListerView
from libs.urlhandler import URLHandler
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QAction,
    QDialog,
    QInputDialog,
    QFormLayout,
    QLabel,
    QListView,
    QApplication,
    QDialogButtonBox,
    QPushButton,
)
from PySide2.QtGui import QStandardItemModel, QStandardItem


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RSS Feed")
        self.setGeometry(300, 300, 440, 640)
        self.center()
        self.__toolBar = self.menuBar()
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

    def showMainView(self, user_data):
        self._main_view = MainView(self)
        self.loadMenubar()
        self.setCentralWidget(self._main_view)

    def loadMenubar(self):
        bar = self.__toolBar
        bar.setVisible(True)
        user = bar.addMenu("App")
        manageUrls = bar.addMenu("Manage URLs")
        manageGroups = bar.addMenu("Manage Groups")
        manageViews = bar.addMenu("View")

        addURLAction = QAction("Add URL", self)
        addURLAction.setShortcut("Ctrl-N")
        addURLAction.triggered.connect(self.addURLCallback)

        removeURLAction = QAction("Remove URL", self)
        removeURLAction.setShortcut("Ctrl-P")
        removeURLAction.triggered.connect(self.removeURLCallback)

        manageUrls.addAction(addURLAction)
        manageUrls.addAction(removeURLAction)

        addGroupAction = QAction("Add Group", self)
        addGroupAction.setShortcut("Ctrl-Shift-N")
        addGroupAction.triggered.connect(self.addGroupCallback)

        removeGroupAction = QAction("Remove Group", self)
        removeGroupAction.setShortcut("Ctrl-Shift-P")
        removeGroupAction.triggered.connect(self.removeGroupCallback)

        manageGroups.addAction(addGroupAction)
        manageGroups.addAction(removeGroupAction)

        viewAllAction = QAction("View All", self)
        # viewAction.setShortcut("Ctrl-Shift-N")
        viewAllAction.triggered.connect(self.viewAllCallback)

        viewGroupAction = QAction("View Group", self)
        # viewGroupAction.setShortcut("Ctrl-Shift-P")
        viewGroupAction.triggered.connect(self.viewGroupCallback)

        viewPopularAction = QAction("View Popular", self)
        # viewPopularAction.setShortcut("Ctrl-Shift-P")
        viewPopularAction.triggered.connect(self.viewPopularCallback)

        manageViews.addAction(viewAllAction)
        manageViews.addAction(viewGroupAction)
        manageViews.addAction(viewPopularAction)

        exitAction = QAction("Quit", self)
        exitAction.setShortcut("Ctrl-X")
        exitAction.triggered.connect(self.exit_app)

        logoutAction = QAction("Logout", self)
        logoutAction.triggered.connect(self.logoutCallback)
        
        user.addAction(exitAction)
        user.addAction(logoutAction)

    # TODO Move all menubar things to class MenuBar in gui
    def addURLCallback(self):
        text, ok = QInputDialog.getText(self, "Add URL", "Paste URL: ")

        if ok:
            # Here we use URL manager to add this into the database
            urlh = URLHandler()
            if urlh.stringIsURL(text):
                print(text)
            else:
                print('it\'s not a url')


    def removeURLCallback(self):
        prompt = 'List of URLs'
        title = 'Choose URL to remove'
        data = [str(x) for x in range(10)]
        ls = ListerView(prompt, title, data, self)

        if ls.exec_():
            print(ls.getResults())

    def addGroupCallback(self):
        text, ok = QInputDialog.getText(
            self, "Group URL", "Enter group name: ")

        if ok:
            # Here we use GroupManager to add this into the database
            print(text)

    def removeGroupCallback(self):
        prompt = 'List of Groups'
        title = 'Choose group to remove'
        data = [str(x) for x in range(100)]
        ls = ListerView(prompt, title, data, self)

        if ls.exec_():
            print(ls.getResults())
            
    def logoutCallback(self):
        self.showLogin()

    def viewAllCallback(self):
        print("This action is yet to be implemented")

    def viewGroupCallback(self):
        print("This action is yet to be implemented")

    def viewPopularCallback(self):
        print("This action is yet to be implemented")

    def exit_app(self):
        self.close()
