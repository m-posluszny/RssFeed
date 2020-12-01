from PySide2.QtWidgets  import QWidget

class MainWindow(QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('RssFeed')    
        self.show()
        