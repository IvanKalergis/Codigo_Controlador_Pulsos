from PySide2.QtWidgets import QApplication
from gui import Window
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("Creating window...")
    window = Window()
    print("window defined")
    window.show()
    print("Window shown.")
    sys.exit(app.exec_())