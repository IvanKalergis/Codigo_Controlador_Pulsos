import sys
from PySide2.QtCore import QTimer,Qt,Signal,Slot
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
        self.ui.Iterations_start.setMinimum(1) 
        self.ui.Iterations_end.setMaximum(1000000)
        self.ui.Iterations_end.setValue(5)
        self.ui.Iterations_end.setMinimum(self.ui.Iterations_start.value()+1) 
        self.ui.ms.setMaximum(1000000)
        self.ui.ms.setMinimum(1)
        self.ui.Loop_Sequence.setValue(1)
        self.ui.ms.setValue(500) # a normal speed
        self.ui.Run_Sequence.clicked.connect(self.Run_Experiment_Gui)
        self.ui.Stop_Sequence.clicked.connect(self.Stop_Experiment_Gui)

        ########## SIGNALS and connectios ##########
        
          ##### ADDING CHANNELS #####
        self.ui.Add_Channel.clicked.connect(self.add_channel_gui)
        self.PML.adding_flag_to_list.connect(self.update_list_channels)
         
        ######## Adding and varying pulses ##############
        self.PML.error_str_signal.connect(self.show_error_message)
        self.ui.Add_Pulse.clicked.connect(self.add_pulse_gui)
        self.ui.Iterations_start.valueChanged.connect(self.set_max)
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
        channel_count=self.ui.Channel_Identifier.count()
        self.PML.add_channel(channel_tag,delay,channel_label,channel_count)



    @Slot(str) #The @Slot decorator in PySide2 is used to explicitly define a method as a slot, which can be connected to a signal. It improves performance and type safety by specifying the expected argument types.
    def update_list_channels(self, flag_str):
        """
        This function is called when a channel is added to the list.
        It updates the list of channels in the GUI.
        """
        #print(f"Adding channel: {flag_str}")
        self.ui.Channel_List.addItem(flag_str)


    ##### ADDING PULSES ######
    def add_pulse_gui(self):
        """
        This function is called when the user clicks the "Add Pulse" button.
        It checks if the pulse is valid and adds it to the list.
        """
        start_time = self.ui.StartTime.value()
        width = self.ui.Puls_Width.value()
        channel_tag = self.ui.Channel_Pulse.currentIndex() #we get the channel from the gui
        function_str=self.ui.Function.text() #we get the function from the gui
        iteration_range = [self.ui.Iterations_start.value(),self.ui.Iterations_end.value()]
        type_change = self.ui.Type_Change.currentIndex()
        self.PML.add_pulse_to_channel(start_time, width,function_str,iteration_range, channel_tag,type_change)

    def set_max(self): # as soon as I change the value fo the Iteration_start, the Iteration _end, allow numbers bigger than the Iterations_start
        self.ui.Iterations_end.setMinimum(self.ui.Iterations_start.value()+1) 
    
    #### RUN Experiment ####
    def Run_Experiment_Gui(self):
        value_loop=self.ui.Loop_Sequence.value()
        self.PML.Run_experiment(value_loop)
    def Stop_Experiment_Gui(self):
        self.PML.Stop_Experiment()

    @Slot(str)
    def show_error_message(self, error_str):
        """
        This function is called when an error occurs.
        It shows an error message to the user.
        """
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error!")
        dlg.setText(error_str)
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("Creating window...")
    window = Window()
    print("window defined")
    window.show()
    print("Window shown.")
    sys.exit(app.exec_())