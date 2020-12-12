from PySide2.QtCore import QTimer
from PySide2.QtWidgets  import QApplication
from gui.MainWindow import MainWindow
import sys
import signal
import atexit

def sigint_handler(*args):
    """The ability to kill the app from the REPL using Ctrl+C"""
    sys.stderr.write('\r')
    QApplication.quit()

def exit_handler():
    ...
#    from libs.databasehandler import DatabaseHandler
#
#    if DatabaseHandler.dbIsTemp:
#        DatabaseHandler.destroyDatabase()
# NOTE(mateusz): This will become useful someday, I promise
    
def main():
    signal.signal(signal.SIGINT, sigint_handler)
    atexit.register(exit_handler)
    app = QApplication()
    window = MainWindow(app)
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
