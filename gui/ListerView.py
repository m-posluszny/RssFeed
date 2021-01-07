from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QFormLayout, QLabel, QListView, QDialogButtonBox
from PySide2.QtGui import QStandardItemModel, QStandardItem


class ListerView(QDialog):
    def __init__(self,  title, message, items, parent=None):
        super(ListerView, self).__init__(parent=parent)
        form = QFormLayout(self)
        form.addRow(QLabel(message))
        self.listView = QListView(self)
        self.listView.clicked.connect(self.mouseClickEvent)
        form.addRow(self.listView)
        model = QStandardItemModel(self.listView)
        self.setWindowTitle(title)
        for item in items:
            # create an item with a caption
            standardItem = QStandardItem(item)
            standardItem.setCheckable(True)
            standardItem.setEditable(False)
            model.appendRow(standardItem)
        self.listView.setModel(model)

    def mouseClickEvent(self):
        row = [qmi.row() for qmi in self.listView.selectedIndexes()][0]
        item = self.listView.model().item(row)
        checkState = item.checkState()
        if checkState == Qt.Checked:
            checkState = Qt.Unchecked
        else:
            checkState = Qt.Checked
        item.setCheckState(checkState)

    def enableButtonBox(self):
        form = self.layout()
        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getResults(self):
        selected = []
        model = self.listView.model()
        i = 0
        while model.item(i):
            if model.item(i).checkState():
                selected.append(model.item(i).text())
            i += 1
        return selected
