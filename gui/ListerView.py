from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QAction, QDialog, QInputDialog, QFormLayout, QLabel, QListView, QApplication, QDialogButtonBox, QPushButton
from PySide2.QtGui import QStandardItemModel, QStandardItem

class ListerView(QDialog):
	def __init__(self,  title, message, items, parent=None):
		super(ListerView, self).__init__(parent=parent)
		form = QFormLayout(self)
		form.addRow(QLabel(message))
		self.listView = QListView(self)
		form.addRow(self.listView)
		model = QStandardItemModel(self.listView)
		self.setWindowTitle(title)
		for item in items:
			# create an item with a caption
			standardItem = QStandardItem(item)
			standardItem.setCheckable(True)
			model.appendRow(standardItem)
		self.listView.setModel(model)

		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
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
