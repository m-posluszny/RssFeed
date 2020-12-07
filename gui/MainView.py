from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets  import QLabel, QWidget, QLineEdit, QVBoxLayout, QPushButton

class MainView(QWidget):
    
    def __init__(self,parent=None):
        super().__init__(parent)