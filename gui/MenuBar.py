from gui.ListerView import ListerView
from libs.urlhandler import URLHandler
from libs.grouphandler import GroupHandler
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction, QInputDialog, QAction, QDialog,  QInputDialog,  QDialogButtonBox, QHBoxLayout, QVBoxLayout, QWidget


class MenuBar:

    def __init__(self, menuBar, parent=None):
        """
        Constructor of MenuBar which holds all of the functionality that
        can be accessed via the main menu bar of the application.

        Args:
            menuBar (QMenuBar): The actual Qt object of the menu bar
            parent (QWidget): GUI parent of widget. Defaults to None.
        """

        self.bar = menuBar
        self.mainView = None
        self.parent = parent
        self.hide_bar()
        user = self.bar.addMenu("App")
        add_urlAction = QAction("Add URL", parent)
        add_urlAction.triggered.connect(self.add_url_callback)

        remove_urlAction = QAction("Remove URL", parent)
        remove_urlAction.triggered.connect(self.remove_url_callback)
        self.bar.addAction(add_urlAction)
        self.bar.addAction(remove_urlAction)

        add_groupAction = QAction("Add Group", parent)
        add_groupAction.triggered.connect(self.add_group_callback)

        remove_groupAction = QAction("Remove Group", parent)
        remove_groupAction.triggered.connect(self.remove_group_callback)

        self.bar.addAction(add_groupAction)
        self.bar.addAction(remove_groupAction)

        add_urlGroupAction = QAction("Add URL to Group", parent)
        add_urlGroupAction.triggered.connect(self.add_url_to_group_callback)

        remove_urlGroupAction = QAction("Remove URL from Group", parent)
        remove_urlGroupAction.triggered.connect(
            self.remove_url_from_group_callback)

        self.bar.addAction(add_urlGroupAction)
        self.bar.addAction(remove_urlGroupAction)

        showPopularAction = QAction("Show Popular URLs", parent)
        showPopularAction.triggered.connect(self.show_popular_callback)

        self.bar.addAction(showPopularAction)
        exitAction = QAction("Quit", parent)
        exitAction.setShortcut("Ctrl-X")
        exitAction.triggered.connect(self.parent.exit_app)

        logoutAction = QAction("Logout", parent)
        logoutAction.triggered.connect(self.logout_callback)
        user.addAction(exitAction)
        user.addAction(logoutAction)

    def set_main_view(self, view):
        """
        Setter for the mainView field
        """
        self.mainView = view

    def show_bar(self):
        """
        Setter for the boolean value of bar that makes it visible
        """
        self.bar.setVisible(True)

    def hide_bar(self):
        """
        Setter for the boolean value of bar that makes it invisible
        """
        self.bar.setVisible(False)

    def show_popular_callback(self):
        """
        Callback method for the button "Show Popular URLs"
        It handles what things have to happen after the button press
        """
        
        URLHandler.get_most_popular_urls()
        self.mainView.refresh_groups(True)

    def add_url_callback(self):
        """
        Callback method for the button "Add URL"
        It creates a dialog box that the user passes the URL into that is
        later added to the database
        """

        res, ok = QInputDialog.getText(self.parent, "Add URL", "Paste URL: ")
        res = res.strip()
        if ok:
            if URLHandler.string_is_url(res):
                url_added = URLHandler.add_url(res)
                if url_added != -1:
                    index = URLHandler.add_url_to_group(res, 'All')
                    self.mainView.group_view.add_url(res, 'All', index)
            else:
                print('it\'s not a url')

    def remove_url_callback(self):
        """
        Callback method for the button "Remove URL"
        It creates a ListerView that allows the user to mark the
        URLs that are supposed to be remove from the database
        """
        
        prompt = 'List of URLs'
        title = 'Choose URL to remove'

        db = DatabaseHandler()
        data = []
        entries = db.get_entry(CredentialsHandler.lastUsername)
        for index in entries['groups']['All']:
            data.append(entries['urls'][index]['actual_url'])
        ls = ListerView(prompt, title, data, self.parent)
        ls.enable_button_box()

        if ls.exec_():
            reslist = ls.get_results()
            for res in reslist:
                URLHandler.remove_url(res)
                self.mainView.group_view.remove_url(res, "All")

    def add_group_callback(self):
        """
        Callback method for the button "Add group"
        It creates a dialog box that the user passes the group name into
        that is later added to the database
        """

        res, ok = QInputDialog.getText(
            self.parent, "Group URL", "Enter group name: ")
        res = res.strip()
        if ok:
            group_added = GroupHandler.add_group(res)
            if group_added:
                self.mainView.group_view.add_group(res, [], [])

    def remove_group_callback(self):
        """
        Callback method for the button "Remove group"
        It creates a ListerView that allows the user to mark the
        groups that are supposed to be remove from the database
        """
        
        prompt = 'List of Groups'
        title = 'Choose group to remove'

        db = DatabaseHandler()
        entries = db.get_entry(CredentialsHandler.lastUsername)
        data = [url for url in entries['groups']]
        data = self.exclude_groups(data)
        ls = ListerView(prompt, title, data, self.parent)
        ls.enable_button_box()

        if ls.exec_():
            reslist = ls.get_results()
            for res in reslist:
                GroupHandler.remove_group(res)
                self.mainView.group_view.remove_group(res)

    def add_url_to_group_callback(self):
        """
        Callback method for the button "Add url to group"
        It creates a window that allows the user to mark the groups
        that and urls that are supposed to be added to them
        """

        w = QWidget()
        f = QHBoxLayout(w)

        db = DatabaseHandler()
        entries = db.get_entry(CredentialsHandler.lastUsername)

        ldata = [url for url in entries['groups']]
        ldata = self.exclude_groups(ldata)
        ls = ListerView('Groups', 'Groups', ldata, self.parent)

        rdata = []
        for index in entries['groups']['All']:
            rdata.append(entries['urls'][index]['actual_url'])
        rs = ListerView('Urls', 'Urls', rdata, self.parent)

        rs.layout().setContentsMargins(0, 0, 0, 0)
        ls.layout().setContentsMargins(0, 0, 0, 0)
        f.addWidget(ls)
        f.addWidget(rs)

        q = QDialog(self.parent)
        q.setWindowTitle('Add URL to Group')
        mf = QVBoxLayout(q)
        mf.addWidget(w)

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self.parent)
        mf.addWidget(buttonBox)
        buttonBox.accepted.connect(q.accept)
        buttonBox.rejected.connect(q.reject)

        if q.exec_():
            groups = ls.get_results()
            urls = rs.get_results()

            for group in groups:
                for url in urls:
                    index = URLHandler.add_url_to_group(url, group)
                    if index > -1:
                        self.mainView.group_view.add_url(url, group, index)

    def remove_url_from_group_callback(self):
        """
        Callback method for the button "Remove url from group"
        It creates a window that allows the user to mark the groups
        that and urls that are supposed to be removed from them
        """
        
        w = QWidget()
        f = QHBoxLayout(w)

        db = DatabaseHandler()
        entries = db.get_entry(CredentialsHandler.lastUsername)

        ldata = [url for url in entries['groups']]
        ldata = self.exclude_groups(ldata)
        ls = ListerView('Groups', 'Groups', ldata, self.parent)

        rdata = []
        for index in entries['groups']['All']:
            rdata.append(entries['urls'][index]['actual_url'])
        rs = ListerView('Urls', 'Urls', rdata, self.parent)

        rs.layout().setContentsMargins(0, 0, 0, 0)
        ls.layout().setContentsMargins(0, 0, 0, 0)
        f.addWidget(ls)
        f.addWidget(rs)

        q = QDialog(self.parent)
        q.setWindowTitle('Remove URL from Group')
        mf = QVBoxLayout(q)
        mf.addWidget(w)

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self.parent)
        mf.addWidget(buttonBox)
        buttonBox.accepted.connect(q.accept)
        buttonBox.rejected.connect(q.reject)

        if q.exec_():
            groups = ls.get_results()
            urls = rs.get_results()

            for group in groups:
                for url in urls:
                    URLHandler.remove_url_from_group(url, group)
                    self.mainView.group_view.remove_url(url, group)

    def logout_callback(self):
        """
        Callback method for the menu option "Logout"
        Sets the main view back to the login screen
        """

        self.parent.show_login()

    def exclude_groups(self, data):
        """
        Helper method to make sure that the user cannot modify
        the groups that are specified here
        """

        if 'Most Popular URLs' in data:
            data.remove('Most Popular URLs')
        if 'All' in data:
            data.remove('All')
        return data
