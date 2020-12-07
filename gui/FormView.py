from libs.credhandler import CredentialsHandler
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets  import QLabel, QWidget, QLineEdit, QVBoxLayout, QPushButton

class FormView(QWidget):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self._parent = parent
        self._form_layout = QVBoxLayout(self)
        self._form_layout.setContentsMargins(50,50,50,50)
        self._form_layout.setSpacing(30)
        self._user_box = QLineEdit()
        self._user_box.setPlaceholderText("username")
        self._password_box = QLineEdit()
        self._password_box.setPlaceholderText("password")
        self._password_box.setEchoMode(QLineEdit.Password)
        self._widget_label = QLabel("",self)
        self._widget_label.setMaximumHeight(55)
        label_font = QFont("Arial", 35, QFont.Capitalization) 
        input_font = QFont("Arial", 12, QFont.Capitalization) 
        subtext_font = QFont("Arial", 10)
        self._action_button = QPushButton("", self)
        self._action_button.clicked.connect(self.onConfirmPress)
        self._subtext_label = QPushButton("",self)
        self._subtext_label.setMaximumHeight(10)
        self._subtext_label.setFlat(True)
        self._subtext_label.setFont(subtext_font)
        self._subtext_label.clicked.connect(self.onLinkPress)
        self._password_box.setFont(input_font)
        self._user_box.setFont(input_font)
        self._widget_label.setFont(label_font)
        self._widget_label.setAlignment(Qt.AlignCenter)
        self._form_layout.addWidget(self._widget_label)
        self._form_layout.addWidget(self._user_box)
        self._form_layout.addWidget(self._password_box)
        self._form_layout.addWidget(self._action_button)
        self._form_layout.addWidget(self._subtext_label)
        self._form_layout.addStretch()
    
    def returnSuccesfulLogin(self,user_data):
        self._parent.showMainView(user_data)
    
    def onConfirmPress(self,event):
        ...
    
    def onLinkPress(self, event):
        ...
class LoginView(FormView):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self._widget_label.setText("Login")
        self._action_button.setText("Login")
        self._subtext_label.setText("Don't have an account? Register")
        
    def onConfirmPress(self,event):
        username = self._user_box.text()
        password = self._password_box.text()
        credHandler = CredentialsHandler(username,password)
        credHandler.encryptCredentials()
        if not credHandler.areCredValid():
            #getUserArticles
            user_data = []
            self.returnSuccesfulLogin(user_data)
    
    def onLinkPress(self, event):
        self._parent.showRegister()

class RegisterView(FormView):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self._widget_label.setText("Register")
        self._action_button.setText("Register")
        self._subtext_label.setText("Already registered? Login")
    
    
    def onConfirmPress(self,event):
        username = self._user_box.text()
        password = self._password_box.text()
        credHandler = CredentialsHandler(username,password)
        credHandler.encryptCredentials()
        if not credHandler.doesUserExist():
            #getUserArticles
            credHandler.createUser()
            user_data = []
            self.returnSuccesfulLogin(user_data)
    
    def onLinkPress(self, event):
        self._parent.showLogin()
            

    
    