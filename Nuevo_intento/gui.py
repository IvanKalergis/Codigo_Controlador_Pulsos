import sys
from PySide2.QtCore import QTimer,Qt,Signal
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox
)
from PySide2.QtGui import QPen,QColor
import pyqtgraph as pg #para los gráficos de las secuencias
import numpy as np
from Sequence_one import Ui_Form  # Assuming the UI class is named Ui_MainWindow
import os 
os.environ["QT_MAC_WANTS_LAYER"] = "1" # This is needed for macOS Mojave and later
from logic import PulseManagerLogic as PML
class Window(QWidget,Ui_Form):
    def __init__(self):

        super(Window, self).__init__()
        #print("Initializing UI...")
        self.ui = Ui_Form() # initializes the UI form
        self.ui.setupUi(self)    
        self.PML = PML(parent=self)
        #print("UI initialized.")
        self.ui.Delay_ON.setMaximum(1000000)  # Set to a large number as needed
        self.ui.Delay_ON.setMinimum(0)  
        self.ui.Delay_OFF.setMaximum(1000000)
        self.ui.Delay_OFF.setMinimum(0)
        self.ui.StartTime.setMaximum(1000000)
        self.ui.StartTime.setMinimum(0) 
        self.ui.Puls_Width.setMaximum(1000000)
        self.ui.Puls_Width.setMinimum(0)
        self.ui.Puls_Width.setMinimum(1)
        self.ui.Iterations_start.setMaximum(1000000)
        self.ui.Iterations_start.setMinimum(0) 
        self.ui.Iterations_end.setMaximum(1000000)
        self.ui.Iterations_end.setMinimum(self.ui.Iterations_start.value()+1) 
        self.ui.ms.setMaximum(1000000)
        self.ui.ms.setMinimum(1)
        self.ui.Loop_Sequence.setValue(1)
        self.ui.ms.setValue(500) # a normal speed

        ########## SIGNALS and connectios ##########
        
          ##### ADDING CHANNELS #####
        self.ui.Add_Channel.clicked.connect(self.add_channel_gui)
        self.PML.adding_flag_to_list.connect(self.update_list_channels)



        ######## METHODS ##############

            ##### ADDING CHANNELS #####
    def add_channel_gui(self):
        """
        This function is called when the user clicks the "Add Channel" button.
        It checks if the channel is valid and adds it to the list.
        """
        channel_tag = self.ui.Channel_Identifier.currentIndex()
        print(channel_tag)
        delay= [self.ui.Delay_ON.value(),self.ui.Delay_OFF.value()]
        channel_label = self.ui.Type_Channel.text()#we get the label of the channel from the gui
        channel_label=channel_label.lower() #we leave it undercase
        self.PML.add_channel(channel_tag,delay,channel_label)
    def update_list_channels(self, flag_str):
        """
        This function is called when a channel is added to the list.
        It updates the list of channels in the GUI.
        """
        #print(f"Adding channel: {flag_str}")
        self.ui.Channel_List.addItem(flag_str)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("Creating window...")
    window = Window()
    print("window defined")
    window.show()
    print("Window shown.")
    sys.exit(app.exec_())