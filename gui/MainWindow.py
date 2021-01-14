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
        """
        Constructor of MainWindow which represents the actual
        window that the user interacts with
        """

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
        """
        Method for settings the application icon to the one
        that is sorted in the given path
        """
        icon = QIcon('res/icon.png')
        self.setWindowIcon(icon)

    def center(self):
        """
        Method for centering all of the objects that are displayed
        in the window
        """

        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def show_login(self):
        """
        Method for setting the main viewed and main controlling
        to the the login widget
        """

        self.__toolBar.hide_bar()
        self._login_view = LoginView(self)
        self.setCentralWidget(self._login_view)

    def show_register(self):
        """
        Method for setting the main viewed and main controlling
        to the the register widget
        """

        self.__toolBar.hide_bar()
        self._register_view = RegisterView(self)
        self.setCentralWidget(self._register_view)

    def show_feed_view(self):
        """
        Method for setting the main viewed and main controlling
        to the the register widget
        """

        self.__toolBar.show_bar()
        self.mainView = MainView()
        self.__toolBar.set_main_view(self.mainView)
        self.setCentralWidget(self.mainView)

    def exit_app(self):
        """
        Method for exiting from the application loop and thus
        killing the main window
        """

        self.close()
