from PySide2.QtWidgets  import QMainWindow
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
        manage_urls = bar.addMenu("Manage URLs")
        manage_groups = bar.addMenu("Manage Groups")
       
 
        
    
    def exit_app(self):
        self.close()
 
 