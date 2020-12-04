from PySide2.QtWidgets  import QApplication
from gui.MainWindow import MainWindow
from pyside_material import apply_stylesheet
import sys

def main():
    app = QApplication()
    apply_stylesheet(app, theme='dark_amber.xml')
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
