from PySide2.QtWidgets  import QApplication
from gui.MainWindow import MainWindow
import sys

def main():
    app = QApplication()
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
