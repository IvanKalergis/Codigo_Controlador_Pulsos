import sys
#from PyQt5.QtCore import QTimer
#import spinapi
#from spinapi import Inst, ON 
from PySide2.QtCore import QTimer,Qt,Signal
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox
)
#import spinapi
#from spinapi import Inst, ON
from PySide2.QtGui import QPen,QColor
import pyqtgraph as pg #para los gráficos de las secuencias
import numpy as np
from Sequence_one import Ui_Form  # Assuming the UI class is named Ui_MainWindow
import os 
os.environ["QT_MAC_WANTS_LAYER"] = "1" # This is needed for macOS Mojave and later
from logic import Logic
class Window(QWidget,Ui_Form):
    def __init__(self):
        #super().__init__()
        #self.setupUi(self)
        super(Window, self).__init__()
        #print("Initializing UI...")
        self.ui = Ui_Form() # initializes the UI form
        self.ui.setupUi(self)    
        #print("UI initialized.")
        #we create an instance of the logic
        #self.Logic = Logic()
        self.Logic = Logic(parent=self)
        #print("Logic initialized.")
        ## now lets go over the functionality
        #setting some properties
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
        
        ##### ADDING CHANNELS #####
        self.ui.Add_Channel.clicked.connect(self.respect_simulation_Channel_gui)
        self.Logic.adding_list_signal.connect(self.update_list_channels)
        self.Logic.sequence_signals.connect(self.update_graph_channels)
        self.Logic.print_stuff.connect(self.printstuffgui)
        #### clearing the gui #####
        self.ui.Clear_Channels.clicked.connect(self.clear_list_gui)
        ##### ADDING PULSES ######
        self.ui.Add_Pulse.clicked.connect(self.respect_simulation_pulses_gui)
        self.Logic.clearing_graph_signal.connect(self.clear_graph_gui)
        self.Logic.duration_signal.connect(self.duration_setting_gui)
        self.ui.Loop_Sequence.valueChanged.connect(self.calculate_Loop_Duration_gui)
        #FOR VARIATIONS IN ITERATIONS
        self.ui.Iterations_start.valueChanged.connect(self.set_max)
        self.ui.Channel_Pulse.currentTextChanged.connect(self.gui_show_varying_pulses)#when selecting a channel on the self.ui.Channel_Pulse
        self.ui.Add_Channel.clicked.connect(self.gui_show_varying_pulses) # when adding a new channel to the sequence 
        self.ui.Add_Pulse.clicked.connect(self.gui_show_varying_pulses) #when adding a new channel to the sequence
        self.Logic.Pulse_i.connect(self.add_pulsebox)
        self.Logic.iteration_j.connect(self.add_iteration_list)
        self.ui.Add_Change.clicked.connect(self.respect_simulation_Change_Pulse_gui)
        self.Logic.itera_list.connect(self.add_to_list)

        ###SIMULATION
        #now for when we add specific conditions for a pulse
        #first we need to create a global variable which keeps the channel, the pulse, and each iteration range[ [2,[1,[5,9], [14,20]],[3,[[5,9], [14,20]]]]
        self.ui.Update.clicked.connect(self.simulation_gui)
        self.Logic.clear_simulation_graph.connect(self.clear_simulation)
        self.Logic.add_iteration_txt.connect(self.add_iteration_text)
        self.Logic.add_simulation_graph.connect(self.add_simulation_graph_gui)
        self.ui.Stop_Simulation.clicked.connect(self.stop_simulation_gui)

        ##### RUNNING EXPERIMENT ####
        # this we will solve later since they are complex and not truly important for this purposes
        self.ui.Run_Sequence.clicked.connect(self.Run_Experiment_Gui)

    #### ADDING CHANNELS #######
    def respect_simulation_Channel_gui(self):
        #print("added channels working")
        channel = self.ui.Channel_Identifier.currentIndex()
        print(channel)
        delay_on = self.ui.Delay_ON.value()
        delay_off = self.ui.Delay_OFF.value()
        channel_label = self.ui.Type_Channel.text()#we get the label of the channel from the gui
        channel_label=channel_label.lower() #we leave it undercase
        self.Logic.respect_simulation_Channel(channel,delay_on,delay_off,channel_label)
    
    def update_graph_channels(self,plot_data):
        self.ui.Sequence_Diagram.addItem(plot_data)  # Add updated PlotDataItem
    def update_list_channels(self,item):
        self.ui.Channel_List.addItem(item)
    
    
    def printstuffgui(self,listprint):
        print(listprint)
    
    #### clearing the gui #####
    def clear_list_gui(self):
        self.ui.Channel_List.clear()
        self.ui.Sequence_Diagram.clear()
        self.ui.Iteration_list.clear()
        self.ui.Pulses_box.clear()
        self.ui.Simulation.clear()
        self.ui.Duration_Loop.setText("Duration: ( )")
        self.ui.current_iteration.setText("current iteration: ( )")
        self.Logic.clear_list()
    
    ##### ADDING PULSES ######
    def respect_simulation_pulses_gui(self): 
        channel=self.ui.Channel_Pulse.currentIndex()
        start_time= self.ui.StartTime.value()
        width= self.ui.Puls_Width.value() #Pulse_Width
        max_counter= self.ui.Loop_Sequence.value()
        self.Logic.respect_simulation_Pulses(channel,start_time,width,max_counter)
    def clear_graph_gui(self):
        self.ui.Sequence_Diagram.clear()
    def duration_setting_gui(self,duration):
        self.ui.Duration_Loop.setText(duration)
    ###### FOR Variations in iterations #####
    def set_max(self): # as soon as I change the value fo the Iteration_start, the Iteration _end, allow numbers bigger than the Iterations_start
        self.ui.Iterations_end.setMinimum(self.ui.Iterations_start.value()+1) 
        pass  
    def gui_show_varying_pulses(self):
        self.ui.Pulses_box.clear() #as soon as the Channel_box changes the pulse box is cleared and add the pulses for the respective. 
        self.ui.Iteration_list.clear()
        channel_pulse_index=self.ui.Channel_Pulse.currentIndex()
        self.Logic.show_varying_pulses(channel_pulse_index)
        
    def add_pulsebox(self,string): #we add the pulse number to the pulse box
        self.ui.Pulses_box.addItem(string)
    def add_iteration_list(self,string):
        self.ui.Iteration_list.addItem(string)
    def respect_simulation_Change_Pulse_gui(self):
        current_text=self.ui.Pulses_box.currentText()
        index=self.ui.Type_Change.currentIndex()
        funct=self.ui.Function.text()
        iter_range=[self.ui.Iterations_start.value(),self.ui.Iterations_end.value()]
        pulse_flag=[current_text,index,funct,iter_range]
        pulse_box_count=self.ui.Pulses_box.count()
        channel_index_box=self.ui.Channel_Pulse.currentIndex()
        current_pulse=self.ui.Pulses_box.currentIndex()
        max_counter= self.ui.Loop_Sequence.value()
        self.Logic.respect_simulation_Change_Pulse(pulse_flag,pulse_box_count,channel_index_box,current_pulse,max_counter)
    def add_to_list(self,pulse_flag_str):
        self.ui.Iteration_list.addItem(pulse_flag_str)
    ######## Simulation #####
    def simulation_gui(self):
        value_loop=self.ui.Loop_Sequence.value()
        ms_value=self.ui.ms.value()
        self.Logic.simulation(value_loop,ms_value)
    def clear_simulation(self):
        self.ui.Simulation.clear()
    def add_iteration_text(self,text):
        self.ui.current_iteration.setText(text)
    def add_simulation_graph_gui(self,sequence):
        self.ui.Simulation.addItem(sequence)
    def stop_simulation_gui(self):
        self.Logic.stop_simulation()
    def calculate_Loop_Duration_gui(self):
        max_counter= self.ui.Loop_Sequence.value()
        self.Logic.calculate_Loop_Duration(max_counter)



    ####### RUN EXP
    def Run_Experiment_Gui(self):
        value_loop=self.ui.Loop_Sequence.value()
        channel_count=self.ui.Channel_Identifier.count()
        self.Logic.Run_experiment(value_loop,channel_count)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        #print("Creating window...")
        window = Window()
        #print("window defined")
        window.show()
        #print("Window shown.")
    except Exception as e:
        #print(f"Error creating window: {e}")
        sys.exit(1)
    sys.exit(app.exec_())