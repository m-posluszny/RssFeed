from libs.credhandler import CredentialsHandler
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QPalette, QColor
from PySide2.QtWidgets  import QLabel, QWidget, QLineEdit, QVBoxLayout, QPushButton
import re

class FormView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self._form_layout = QVBoxLayout(self)
        self._form_layout.setContentsMargins(50, 50, 50, 50)
        self._form_layout.setSpacing(30)
        self._user_box = QLineEdit()
        self._user_box.setPlaceholderText("username")
        self._password_box = QLineEdit()
        self._password_box.setPlaceholderText("password")
        self._password_box.setEchoMode(QLineEdit.Password)
        self._widget_label = QLabel("", self)
        self._widget_label.setMaximumHeight(55)
        label_font = QFont("Arial", 35, QFont.Capitalization)
        error_font = QFont("Arial", 18, QFont.Capitalization)
        input_font = QFont("Arial", 12, QFont.Capitalization)
        subtext_font = QFont("Arial", 10)
        self._action_button = QPushButton("", self)
        self._action_button.clicked.connect(self.onConfirmPress)
        self._action_button.setAutoDefault(True)
        self._subtext_label = QPushButton("", self)
        self._subtext_label.setMaximumHeight(10)
        self._subtext_label.setFlat(True)
        self._subtext_label.setFont(subtext_font)
        self._subtext_label.clicked.connect(self.onLinkPress)
        self._password_box.setFont(input_font)
        self._user_box.setFont(input_font)
        self._widget_label.setFont(label_font)
        self._widget_label.setAlignment(Qt.AlignCenter)
        self._error_palette = QPalette()
        self._error_palette.setColor(QPalette.Foreground, QColor("red"))
        self._error_palette.setColor(QPalette.Background, QColor("red"))
        self._error_message = QLabel("", self)
        self._error_message.setStyleSheet("QLabel { color : red; }")
        self._error_message.setFont(error_font)
        self._error_message.setAlignment(Qt.AlignLeft)
        self._error_message.setVisible(False)
        self._form_layout.addWidget(self._widget_label)
        self._form_layout.addWidget(self._error_message)
        self._form_layout.addWidget(self._user_box)
        self._form_layout.addWidget(self._password_box)
        self._form_layout.addWidget(self._action_button)
        self._form_layout.addWidget(self._subtext_label)
        self._form_layout.addStretch()

    def returnSuccesfulLogin(self):
        self._parent.showFeedView()

    def onConfirmPress(self, event):
        ...

    def onLinkPress(self, event):
        ...

    def displayErrorMessage(self):
        self._error_message.setVisible(True)


class LoginView(FormView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._widget_label.setText("Login")
        self._action_button.setText("Login")
        self._error_message.setText("ERROR")
        self._subtext_label.setText("Don't have an account? Register")

    def onConfirmPress(self, event):
        username = self._user_box.text()
        password = self._password_box.text()

        if len(username) > 0 and len(password) > 0:
            userpassregex = '([a-z]|[0-9]|\.)*'
            resu = re.match(userpassregex, username)
            resp = re.match(userpassregex, password)
            if resu.span()[1] == len(resu.string) and resp.span()[1] == len(resp.string):
                credHandler = CredentialsHandler(username,password)
                credHandler.encryptCredentials()
                if credHandler.areCredValid():
                    self.returnSuccesfulLogin()
                else:
                    self._error_message.setText("Failed to login, bad credentials")
                    self.displayErrorMessage()
            else:
                self._error_message.setText("Invalid characters, use only a-z, 0-9 and periods (.)")
                self.displayErrorMessage()

    
    def onLinkPress(self, event):
        self._parent.showRegister()


class RegisterView(FormView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._widget_label.setText("Register")
        self._action_button.setText("Register")
        self._error_message.setText("ERROR")
        self._subtext_label.setText("Already registered? Login")

    def onConfirmPress(self, event):
        username = self._user_box.text()
        password = self._password_box.text()
        if len(username) > 0 and len(password) > 0:
            userpassregex = '([a-z]|[0-9]|\.)*'
            resu = re.match(userpassregex, username)
            resp = re.match(userpassregex, password)
            if resu.span()[1] == len(resu.string) and resp.span()[1] == len(resp.string):
                credHandler = CredentialsHandler(username,password)
                credHandler.encryptCredentials()
                if not credHandler.doesUserExist():
                    credHandler.createUser()
                    self.returnSuccesfulLogin()
                else:
                    self.displayErrorMessage()
                    self._error_message.setText("Login exists, pick different one")
            else:
                self._error_message.setText("Invalid characters, use only a-z, 0-9 and periods (.)")
                self.displayErrorMessage()

    def onLinkPress(self, event):
        self._parent.showLogin()
