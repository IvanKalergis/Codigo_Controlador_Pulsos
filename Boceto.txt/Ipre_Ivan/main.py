import sys
from PySide2.QtCore import QTimer,Qt
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox
)
from Gui import Window
"""here we initialize the gui"""
app = QApplication(sys.argv)
window = Window()
window.show()


sys.exit(app.exec_())
