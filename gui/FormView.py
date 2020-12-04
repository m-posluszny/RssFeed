from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets  import QLabel, QWidget, QLineEdit, QVBoxLayout, QPushButton

class FormView(QWidget):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.form_layout = QVBoxLayout(self)
        self.user_box = QLineEdit()
        self.user_box.setPlaceholderText("username")
        self.password_box = QLineEdit()
        self.password_box.setPlaceholderText("password")
        self.password_box.setEchoMode(QLineEdit.Password)
        self.widget_label = QLabel("Test",self)
        self.widget_label.setMaximumHeight(55)
        label_font = QFont("Arial", 35, QFont.Capitalization) 
        input_font = QFont("Arial", 12, QFont.Capitalization) 
        self.password_box.setFont(input_font)
        self.user_box.setFont(input_font)
        self.widget_label.setFont(label_font)
        self.widget_label.setAlignment(Qt.AlignCenter)
        self.form_layout.addWidget(self.widget_label)
        self.form_layout.addWidget(self.user_box)
        self.form_layout.addWidget(self.password_box)
        
class LoginView(FormView):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        button = QPushButton("Login", self)
        self.widget_label.setText("Login")
        self.form_layout.addWidget(button)

class RegisterView(FormView):
    
    def __init__(self,parent=None):
        super().__init__("Register",parent)
        self.widget_label.setText("Register")
        button = QPushButton("Register", self)
        self.form_layout.addWidget(button)