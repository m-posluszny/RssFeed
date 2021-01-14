from libs.credhandler import CredentialsHandler
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QPalette, QColor
from PySide2.QtWidgets import QLabel, QWidget, QLineEdit, QVBoxLayout, QPushButton
import re


class FormView(QWidget):

    def __init__(self, parent=None):
        """
        Constructor of FormView which creates a new widget that has two entry boxes,
        a button and a link to which you can attach a callback
        
        Args:
            parent (QWidget): GUI parent of widget. Defaults to None.
        """

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
        self._action_button.clicked.connect(self.on_confirm_press)
        self._action_button.setAutoDefault(True)
        self._subtext_label = QPushButton("", self)
        self._subtext_label.setMaximumHeight(10)
        self._subtext_label.setFlat(True)
        self._subtext_label.setFont(subtext_font)
        self._subtext_label.clicked.connect(self.on_link_press)
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

    def return_succesful_login(self):
        """
        Method called when the login was succesful and we change the shown
        widget to the FeedView one
        """
        self._parent.show_feed_view()

    def on_confirm_press(self, event):
        """
        Callback method called when the button is pressed
        Here it's not doing anything
        """

        pass

    def on_link_press(self, event):
        """
        Callback method called when the link is pressed
        Here it's not doing anything
        """

        pass

    def display_error_message(self):
        """
        Method for making the error message widget visible
        """

        self._error_message.setVisible(True)


class LoginView(FormView):

    def __init__(self, parent=None):
        """
        Constructor of LoginView which constructs a FormView with login
        elements
        
        Args:
            parent (QWidget): GUI parent of widget. Defaults to None.
        """

        super().__init__(parent)
        self._widget_label.setText("Login")
        self._action_button.setText("Login")
        self._error_message.setText("ERROR")
        self._subtext_label.setText("Don't have an account? Register")

    def on_confirm_press(self, event):
        """
        Method override for the callback when the button is pressed
        It checkes wether the given login and password by the user is correct
        and either calls 'return_succesful_login' or 'display_error_message'
        """

        username = self._user_box.text()
        password = self._password_box.text()

        if len(username) > 0 and len(password) > 0:
            userpassregex = '([a-z]|[0-9]|\.)*'
            resu = re.match(userpassregex, username)
            resp = re.match(userpassregex, password)
            if resu.span()[1] == len(resu.string) and resp.span()[1] == len(resp.string):
                credHandler = CredentialsHandler(username, password)
                credHandler.encrypt_credentials()
                if credHandler.are_cred_valid():
                    self.return_succesful_login()
                else:
                    self._error_message.setText(
                        "Failed to login, bad credentials")
                    self.display_error_message()
            else:
                self._error_message.setText(
                    "Invalid characters, use only a-z, 0-9 and periods (.)")
                self.display_error_message()

    def on_link_press(self, event):
        """
        Method override for the callback when the link is pressed
        It changes the current widget to be the RegisterView
        """
        
        self._parent.show_register()


class RegisterView(FormView):

    def __init__(self, parent=None):
        """
        Constructor of RegisterView which constructs a FormView with
        register elements
        
        Args:
            parent (QWidget): GUI parent of widget. Defaults to None.
        """

        super().__init__(parent)
        self._widget_label.setText("Register")
        self._action_button.setText("Register")
        self._error_message.setText("ERROR")
        self._subtext_label.setText("Already registered? Login")

    def on_confirm_press(self, event):
        """
        Method override for the callback when the button is pressed
        It checkes wether the given login is possible and doesn't exist
        if so it creates the user and calls 'return_succesful_login'
        or if not 'display_error_message'
        """

        username = self._user_box.text()
        password = self._password_box.text()
        if len(username) > 0 and len(password) > 0:
            userpassregex = '([a-z]|[0-9]|\.)*'
            resu = re.match(userpassregex, username)
            resp = re.match(userpassregex, password)
            if resu.span()[1] == len(resu.string) and resp.span()[1] == len(resp.string):
                credHandler = CredentialsHandler(username, password)
                credHandler.encrypt_credentials()
                if not credHandler.does_user_exist():
                    credHandler.create_user()
                    self.return_succesful_login()
                else:
                    self.display_error_message()
                    self._error_message.setText(
                        "Login exists, pick different one")
            else:
                self._error_message.setText(
                    "Invalid characters, use only a-z, 0-9 and periods (.)")
                self.display_error_message()

    def on_link_press(self, event):
        """
        Method override for the callback when the link is pressed
        It changes the current widget to be the LoginView
        """

        self._parent.show_login()
