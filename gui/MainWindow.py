from PySide2.QtWidgets  import QMainWindow
from gui.FormView import LoginView, RegisterView
class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RSS Feed")
        self.setGeometry(300,300,440,640)
        self.setContentsMargins(5,5,5,5)
        self.showLogin()   
        self.show()
        
    def showLogin(self):
        self.login_view = LoginView(self)
        self.setCentralWidget(self.login_view)
    

    def loadMenubar(self):
        self.toolBar = bar = self.menuBar()
        user = bar.addMenu("App")
        refresh = bar.addAction("Refresh Feed")
        refresh_group = bar.addMenu("Refresh Group")
        manage_urls = bar.addMenu("Manage URLs")
        manage_groups = bar.addMenu("Manage Groups")
       
    def exit_app(self):
        self.close()
 
 