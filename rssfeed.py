from PySide2.QtCore import QTimer
from PySide2.QtWidgets  import QApplication
from gui.MainWindow import MainWindow
import sys
import signal

def sigint_handler(*args):
    """The ability to kill the app from the REPL using Ctrl+C"""
    sys.stderr.write('\r')
    QApplication.quit()

def main():

    app = QApplication()
    window = MainWindow(app)

    signal.signal(signal.SIGINT, sigint_handler)
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
