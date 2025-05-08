from logic import PulseManagerLogic
from gui import Window
from PySide2.QtWidgets import QApplication
import sys

class PulseManager:


    def __init__(self):

        self.gui = Window()
        self.logic = PulseManagerLogic()

        self.connect_gui_to_logic()

        self.show()

    def connect_gui_to_logic(self):

        ##### ADDING CHANNELS #####
        self.gui.add_channel_signal.connect(self.logic.add_channel)
        self.logic.adding_flag_to_list.connect(self.gui.update_list_channels)

        ##### MISC #####
        self.logic.error_str_signal.connect(self.gui.show_error_message)

    def show(self):
        
        self.gui.show()
        self.gui.raise_()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    pm = PulseManager()
    sys.exit(app.exec_())