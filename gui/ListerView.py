from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QFormLayout, QLabel, QListView, QDialogButtonBox
from PySide2.QtGui import QStandardItemModel, QStandardItem


class ListerView(QDialog):
    def __init__(self,  title, message, items, parent=None):
        """
        Constructor of ListerView which creates a new dialog with
        scrolled items which the user can mark
        
        Args:
            title (str): The dialog title that should appear
            message (str): The message that the user will see at the top of the dialog
            items ([str]): A list of strings that will be showns as options
        """

        super(ListerView, self).__init__(parent=parent)
        form = QFormLayout(self)
        form.addRow(QLabel(message))
        self.listView = QListView(self)
        self.listView.clicked.connect(self.mouse_click_event)
        form.addRow(self.listView)
        model = QStandardItemModel(self.listView)
        self.setWindowTitle(title)
        for item in items:
            standardItem = QStandardItem(item)
            standardItem.setCheckable(True)
            standardItem.setEditable(False)
            model.appendRow(standardItem)
        self.listView.setModel(model)

    def mouse_click_event(self):
        """
        Callback method that will trigger then the user presses a mouse button
        while hovering over an item
        """

        row = [qmi.row() for qmi in self.listView.selectedIndexes()][0]
        item = self.listView.model().item(row)
        checkState = item.checkState()
        if checkState == Qt.Checked:
            checkState = Qt.Unchecked
        else:
            checkState = Qt.Checked
        item.setCheckState(checkState)

    def enable_button_box(self):
        """
        Method for enabling the buttons the bottom that correspond to OK and Cancel
        """

        form = self.layout()
        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def get_results(self):
        """
        Method for quering the results of the user markings
        The result is a list of strings
        """

        selected = []
        model = self.listView.model()
        i = 0
        while model.item(i):
            if model.item(i).checkState():
                selected.append(model.item(i).text())
            i += 1
        return selected
