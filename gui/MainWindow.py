from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QAction, QDialog, QInputDialog, QFormLayout, QLabel, QListView, QApplication, QDialogButtonBox, QPushButton
from PySide2.QtGui import QStandardItemModel, QStandardItem

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RSS Feed")
        self.setGeometry(300,300,400,600)
        self.showView()
        
    def showView(self):
        self.loadMenubar()
        self.show()

    def loadMenubar(self):
        self.toolBar = bar = self.menuBar()
        user = bar.addMenu("App")
        manageUrls = bar.addMenu("Manage URLs")
        manageGroups = bar.addMenu("Manage Groups")

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

        exitAction = QAction("Quit", self)
        exitAction.setShortcut("Ctrl-X")
        exitAction.triggered.connect(self.exit_app)

        user.addAction(exitAction)
        

    def addURLCallback(self):
        text, ok = QInputDialog.getText(self, "Add URL", "Paste URL: ")

        if ok:
            # Here we use URL manager to add this into the database
            print(text)

    def removeURLCallback(self):
        dialog = QDialog(parent=self)
        form = QFormLayout(dialog)
        form.addRow(QLabel("List of URLs"))
        listView = QListView(dialog)
        form.addRow(listView)
        model = QStandardItemModel(listView)
        self.setWindowTitle('Choose URL to remove')
        # Those are going to be URLs taken from the database
        for item in [str(x) for x in range(10)]:
              standardItem = QStandardItem(item)
              standardItem.setCheckable(True)
              model.appendRow(standardItem)
        listView.setModel(model)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            selected = []
            model = listView.model()
            i = 0
            while model.item(i):
                if model.item(i).checkState():
                    selected.append(model.item(i).text())
                i += 1

            print(selected)

    def addGroupCallback(self):
        text, ok = QInputDialog.getText(self, "Group URL", "Enter group name: ")

        if ok:
            # Here we use GroupManager to add this into the database
            print(text)

    def removeGroupCallback(self):
        dialog = QDialog(parent=self)
        form = QFormLayout(dialog)
        form.addRow(QLabel("List of Groups"))
        listView = QListView(dialog)
        form.addRow(listView)
        model = QStandardItemModel(listView)
        self.setWindowTitle('Choose group to remove')
        # Those are going to be URLs taken from the database
        for item in [str(x) for x in range(100)]:
              standardItem = QStandardItem(item)
              standardItem.setCheckable(True)
              model.appendRow(standardItem)
        listView.setModel(model)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            selected = []
            model = listView.model()
            i = 0
            while model.item(i):
                if model.item(i).checkState():
                    selected.append(model.item(i).text())
                i += 1

            print(selected)
    
    def unimplementedButton(self):
        print("This action is yet to be implemented")

    def exit_app(self):
        self.close()
