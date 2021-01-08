from gui.ListerView import ListerView
from libs.urlhandler import URLHandler
from libs.grouphandler import GroupHandler
from libs.credhandler import CredentialsHandler
from libs.databasehandler import DatabaseHandler
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction, QInputDialog, QAction, QDialog,  QInputDialog,  QDialogButtonBox, QHBoxLayout, QVBoxLayout, QWidget



class MenuBar:

    def __init__(self, menuBar, parent=None):
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
        self.mainView = view

    def show_bar(self):
        self.bar.setVisible(True)

    def hide_bar(self):
        self.bar.setVisible(False)

    def show_popular_callback(self):
        URLHandler.get_most_popular_urls()
        self.mainView.refresh_groups()

    def add_url_callback(self):
        res, ok = QInputDialog.getText(self.parent, "Add URL", "Paste URL: ")

        if ok:
            if URLHandler.string_is_url(res):
                url_added = URLHandler.add_url(res)
                if url_added:
                    index = URLHandler.add_url_to_group(res, 'All')
                    self.mainView.group_view.add_url(res, 'All', index)
            else:
                print('it\'s not a url')

    def remove_url_callback(self):
        prompt = 'List of URLs'
        title = 'Choose URL to remove'

        db = DatabaseHandler()
        entries = db.get_entry(CredentialsHandler.lastUsername)
        data = [url['actual_url'] for url in entries['urls']]
        ls = ListerView(prompt, title, data, self.parent)
        ls.enable_button_box()

        if ls.exec_():
            reslist = ls.get_results()
            for res in reslist:
                URLHandler.remove_url(res)
                self.mainView.group_view.remove_url(res, "All")

    def add_group_callback(self):
        res, ok = QInputDialog.getText(
            self.parent, "Group URL", "Enter group name: ")
        if ok:
            print(res)
            group_added = GroupHandler.add_group(res)
            if group_added:
                self.mainView.group_view.add_group(res, [], [])

    def remove_group_callback(self):
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
        w = QWidget()
        f = QHBoxLayout(w)

        db = DatabaseHandler()
        entries = db.get_entry(CredentialsHandler.lastUsername)

        ldata = [url for url in entries['groups']]
        ldata = self.exclude_groups(ldata)
        ls = ListerView('Groups', 'Groups', ldata, self.parent)

        rdata = [url['actual_url'] for url in entries['urls']]
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
        w = QWidget()
        f = QHBoxLayout(w)

        db = DatabaseHandler()
        entries = db.get_entry(CredentialsHandler.lastUsername)

        ldata = [url for url in entries['groups']]
        ldata = self.exclude_groups(ldata)
        ls = ListerView('Groups', 'Groups', ldata, self.parent)

        rdata = [url['actual_url'] for url in entries['urls']]
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
        self.parent.show_login()

    
    def exclude_groups(self,data):
        if 'Most Popular URLs' in data:
            data.remove('Most Popular URLs')
        if 'All' in data:
            data.remove('All')
        return data
