from gui.MainView import MainView
from gui.FormView import LoginView, RegisterView
from gui.MenuBar import MenuBar
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QMainWindow
)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RSS Feed")
        self.setGeometry(300, 300, 850, 500)
        self.setMinimumSize(850, 500)
        self.center()
        self._register_view = None
        self._login_view = None
        self.__toolBar = MenuBar(self.menuBar(), self)
        self.set_icon()
        self.show_login()
        self.show()

    def set_icon(self):
        icon = QIcon('res/icon.png')
        self.setWindowIcon(icon)

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def show_login(self):
        self.__toolBar.hide_bar()
        self._login_view = LoginView(self)
        self.setCentralWidget(self._login_view)

    def show_register(self):
        self.__toolBar.hide_bar()
        self._register_view = RegisterView(self)
        self.setCentralWidget(self._register_view)

    def show_feed_view(self):
        self.__toolBar.show_bar()
        self.mainView = MainView()
        self.__toolBar.set_main_view(self.mainView)
        self.setCentralWidget(self.mainView)

    def exit_app(self):
        self.close()
