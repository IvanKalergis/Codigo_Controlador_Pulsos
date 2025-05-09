from Channel_class import Channel
from experiment import Experiment
from Frame import Frame
import sys
#from PyQt5.QtCore import QTimer
#import spinapi
#from spinapi import Inst, ON 
from PySide2.QtCore import QTimer,Qt
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox
)

from PySide2.QtGui import QPen,QColor
import pyqtgraph as pg #para los gráficos de las secuencias
import numpy as np
from PySide2.QtCore import QObject , Signal
#for the pulse blaster
#import spinapi
#from spinapi import Inst, LOOP, CONTINUE, END_LOOP, STOP
#for the NI
import nidaqmx
from nidaqmx.constants import (
                                VoltageUnits,
                                AcquisitionType, 
                                TimeUnits, 
                                Level, 
                                Edge, 
                                CountDirection,
                                TriggerType
    )

class PulseManagerLogic(QObject):

    error_str_signal = Signal(str)

    def __init__(self, parent=None):
        super(PulseManagerLogic, self).__init__()
        self.parent = parent  # Store the parent widget):
        self.added_channel_tags= [] # This is the list of the tags of the channels that are added to the database, used to be seld.added_channels
        self.channels = [] # alist with all the createdi instances of the channels
        self.channel_labels = [] # Find a way to get rid of these extra variables
        self.Delays_channel = [] # Find a way to get rid of these extra variables
        self.Experiment_Hub=[] # list of objects were each object is a 
        self.Max_end_time =0 # It gives you the max end time of all iterations
        self.dev = 'Dev1' #el device con su number
        self.counter_pin = 'ctr0' #ctr= counter basicamente una parte de la nih que cuenta o emite cuentas. El gate le dice en que intervalo contar
        self.gate_pin = 'PFI9'

    ##### Adding a channel ####
    adding_flag_to_list=Signal(str)
    def add_channel(self, channel_tag, channel_delay,channel_label,channel_count): # Only function is to add the channel to the database if the conditions are met, it communicates with the GUI
        """
        Adds a channel to the database.
        """
        # Logic to add a channel to the database
        channel_tag=int(channel_tag)
        flag= [channel_tag,channel_delay,channel_label]
        
        if channel_tag not in self.added_channel_tags:  # Check if channel is already added, #flag[0]
            # This is for the Graphs in the Sequence Plot
            if channel_label in ["green", "yellow", "red", "apd", "microwave","blue","pink","orange"]:
                flag_str = f"channel: {flag[0]}, delay_on: {abs(flag[1][0])}, delay_off: {abs(flag[1][1])}, {flag[2]}"  # Convert list to string
                self.adding_flag_to_list.emit(flag_str) #emit the signal to the GUI
                channel_binary=self.convert_to_binary(channel_tag,channel_count)#channel count is the amount of ports in the ni
                self.added_channel_tags.append(flag[0]) #add channel to the set
                channel = Channel(channel_tag,channel_binary,channel_label, channel_delay)
                self.channels.append(channel) 
                self.channels=sorted(self.channels, key=lambda ch: ch.tag) # we order the self.channels list by their tag value
                print(f"channel color: {channel.label}")

                
            else: 
                #print('Emitted')
                self.error_str_signal.emit(f"Label {channel_label} not recognized. Please use one of the following: green, yellow, red, apd, microwave")
        else: 
            self.error_str_signal.emit(f"Channel {channel_tag} already added")

        return flag

    def convert_to_binary(self, channel_tag,channel_count):
        """ We need to conver the channel tag index into a binary number for the pulse blaster
            it's better to do this now than later because, later would require for loops on the experiments methods
            and it will be inneficient.
    
            Given the total number of channels and a target channel_tag (index),
            return the decimal value corresponding to only that channel being activated.

            Args:
                channel_count (int): Total number of channels (length of the bitmask).
                channel_tag (int): Index of the channel to activate (0-based).

            Returns:
                int: Decimal value of the binary number with only channel_tag set to 1.
            """
        if channel_tag >= channel_count or channel_tag < 0:
            raise ValueError("channel_tag must be within the range of available channels.")

        binary = [0] * channel_count
        binary[-(channel_tag + 1)] = 1  # Activate the correct bit from the right
        binary_str = ''.join(map(str, binary))
        decimal= int(binary_str, 2)
        return decimal
    



    #in this method we must target the channel instances already created,
    error_str_signal = Signal(str)
    def add_pulse_to_channel(self, start_time, width,function_width,function_start, iteration_range,channel_tag):
        """ here we check if we got a channel to add the pulse, then we call a method of the channels class, that creates a sequence per iteration."""
        #check if we got a channel to add the pulse
        if len(self.channels)==0:
            self.error_str_signal.emit("No channels added")
            return
        elif channel_tag not in self.added_channel_tags:
            self.error_str_signal.emit(f"Channel {channel_tag} not added")
            
        elif channel_tag in self.added_channel_tags:    
            for channel in self.channels:
                if channel.tag == channel_tag:
                    max_end_time_added_sequence=channel.a_sequence(start_time,width,function_width,function_start,iteration_range)
                    channel.error_adding_pulse_channel.connect(self.error_str_signal.emit)
                    break
            if max_end_time_added_sequence>self.Max_end_time:
                self.Max_end_time=max_end_time_added_sequence
        print(f"self.Max_end_time:{self.Max_end_time}")

    


    def Run_experiment(self,value_loop):

        """ here we iterate through each iteration of the loop to find the channels that have a sequence for that iteration 
            then we order the pulses form the channels that have pulses in this iteration. Then we create an object from the  
            class experiment. which we then add to our list Experiment_Hub
        """
        for i in range(1,value_loop+1): #we iterate per each iteration of the experiment. Iterations start from the value 1
            print(f"iteration for creation of exp:{i}")
            Exp_i_pb=[]
            for channel in self.channels:
                print("Inside the channel loop")
                list_channel_sequence=channel.a_experiment(i)
                if list_channel_sequence!=None: 
                    Exp_i_pb.append(list_channel_sequence)
            exp=Experiment(Exp_i_pb,i)
            exp.Prepare_Exp()
            self.Experiment_Hub.append(exp)  #since we are going from 0-end loop the exp objects will be ordered
        """ Con la lista Experiment_hub ya completa, flateamos la lista, y luego le enviamos los pulsos a la pulse Blaster """
        # Flatten all the pulses into one list
        Flat_exp= [pulse for exp in self.Experiment_Hub for pulse in exp.pb_sequence]
        print(f"len(flat_exp):{Flat_exp}")

        self.Send_to_Pulse_Blaster(Flat_exp)
        """"
        Here we should add a fucntion to recieve the photon count
        
        """
        """counter=self.create_counter_task()
        counter.start()
        timeout = (value_loop*10*1.2) #el el timepo total del experimento *1.2
        spinapi.pb_start()
        for channel in self.channels:
            if channel.label=='apd':
                counts = counter.read(value_loop,timeout=timeout)
                count_0=counts[0]
                counts = np.diff(counts) # instead of accumulating values ex (5,11,21) it gives (5,6,10)
                print(counts)"""
       
        



    def Send_to_Pulse_Blaster(self,Flat_exp):
        """
        Here we recieve the flat list with all the pulses, which we then sent to the PB
        Even if there nos laser device for example apd, it will not through an error and,
        just continue to the next instruction after the give time.
        """
        """spinapi.pb_close()
        spinapi.pb_select_board(0)
        if spinapi.pb_init() != 0:
            #####print("Error initializing board: %s" %pb_get_error())
            input("Please press a key to continue.")
            exit(-1)
        spinapi.pb_reset() 
        spinapi.pb_core_clock(500)
        spinapi.pb_start_programming(spinapi.PULSE_PROGRAM)
        start=spinapi.pb_inst_pbonly(int(sum(Flat_exp[0].channel_binary[0])),Inst.LOOP,1,(Flat_exp[0].end_tail-Flat_exp[0].start_tail)*spinapi.us) # generates a loop of instruction here only one iteration
        """
        print(f"Flat_exp[0].channel_binary:{Flat_exp[0].channel_binary[0]}")
        print(f"spinapi.pb_inst_pbonly({sum(Flat_exp[0].channel_binary[0])},Inst.LOOP,{1},({Flat_exp[0].end_tail-Flat_exp[0].start_tail})*spinapi.us)") 
        for i in range(1,len(Flat_exp)):# we start from one because we already did the 0 index
            if i!=len(Flat_exp) -1:
                print(f"spinapi.pb_inst_pbonly({sum(list(Flat_exp[i].channel_binary[0]))},Inst.CONTINUE,0,({Flat_exp[i].end_tail-Flat_exp[i].start_tail})*spinapi.us)")
                #spinapi.pb_inst_pbonly(int(sum(Flat_exp[i].channel_binary[0])),Inst.CONTINUE,0,(Flat_exp[i].end_tail-Flat_exp[i].start_tail)*spinapi.us)
            else:
                print(f"spinapi.pb_inst_pbonly({sum(list(Flat_exp[i].channel_binary[0]))},Inst.CONTINUE,0,({Flat_exp[i].end_tail-Flat_exp[i].start_tail})*spinapi.us)")
                #spinapi.pb_inst_pbonly(int(sum(Flat_exp[i].channel_binary[0])),Inst.CONTINUE,0,(Flat_exp[i].end_tail-Flat_exp[i].start_tail)*spinapi.us)
                print(f"spinapi.pb_inst_pbonly({sum(list(Flat_exp[i].channel_binary[0]))},Inst.END_LOOP,start,{Flat_exp[i].end_tail-Flat_exp[i].start_tail}")
                #spinapi.pb_inst_pbonly(int(sum(Flat_exp[i].channel_binary[0])),Inst.END_LOOP,start,Flat_exp[i].end_tail-Flat_exp[i].start_tail)
        #spinapi.pb_inst_pbonly(int(0),Inst.STOP,0,1*spinapi.us) # This instruction stops the pulse sequence. The duration is set to a very small value to ensure the stop instruction is executed almost immediately.
        print(f"spinapi.pb_inst_pbonly(int(0),Inst.STOP,0,0.01*spinapi.us)")
        #spinapi.pb_stop_programming()  # This function call signals the end of programming the pulse sequence. It tells the SpinAPI library that the sequence definition is complete and the pulse program can be finalized
        print(f"spinapi.pb_stop_programming()")
        #spinapi.pb_reset() 
        pass 
    # To recieve the counts from the apd
    def create_counter_task(self):
        """
        Todo este task es para la ni"""
        #creamos el task que lee las cuentas
        counter_task=nidaqmx.Task(new_task_name='T1 APD fluorescence counts') # crear el task
        #En que canal recivir las cuentas y bajo que condiciones
        counter_task.ci_channels.add_ci_count_edges_chan(
            counter=self.dev + '/' + self.counter_pin, #pin APD en la ni, en este caso seria pin 8
            name_to_assign_to_channel='APD',
            edge= Edge.RISING,
            initial_count=0,
            count_direction=CountDirection.COUNT_UP
        ) #ci=counter input, edges cuenta cada vez que hay una subida o bajada de una señal
        #el cuando recibir las cuentas
        counter_task.timing.cfg_samp_clk_timing(
            rate=100,
            source='/' + self.dev + '/' + self.gate_pin,#cuenta segu cuando llegan las señales del gate
            active_edge=Edge.FALLING, # empieza acontar cuando la señal gate baja
            sample_mode=AcquisitionType.CONTINUOUS,
            samps_per_chan=100000)
        #una continuiacion de lo de arriba
        counter_task.triggers.pause_trigger.dig_lvl_src=self.gate_pin
        counter_task.triggers.pause_trigger.dig_lvl_when=Level.LOW # que pause de contar cuando este en low
        counter_task.triggers.pause_trigger.trig_type=TriggerType.DIGITAL_LEVEL

        return counter_task
        
        
    def Stop_Experiment(self): 
        """spinapi.pb_stop() #stop de program
        spinapi.pb_close() # close the pusle blaster, becasue when you want to open it again it must be close for this"""
        pass



    # ••••• DISPLAY Selected Frame ••••••••
    add_frame_to_graph=Signal(pg.PlotDataItem)
    def Prepare_Frame(self,frame_i):
        """Each time we change the value of the frame, it shows the corresponding frame in the graph
            for this we need to first identify and obtain the pulses of channes who have a sequence 
            for that iterations"""
        sequences_all_channels=[]
        tags_colors=[]
        for channel in self.channels:
            pulses_channel=channel.a_display(frame_i) #checks in the respective channel instance if it has a sequence for this frame, if it has a a sequence active_check will hold the pb_pulses
            if pulses_channel!=None: #meaning there is a sequence in this channel per the iteration i
                sequences_all_channels.append(pulses_channel)
                tags_colors.append([channel.tag,channel.label])
                pass
        frame=Frame(tags_colors,sequences_all_channels,frame_i,self.Max_end_time)
        frame.Display_Frame() # here we send the value to build the Frame
        sequence_for_graph=frame.PlotSequences
        for sequence_frame in sequence_for_graph:
            self.add_frame_to_graph.emit(sequence_frame)
    
    
    # ••••• DISPLAY a simulation of all frames ••••••••
    next_frame_signal=Signal(int)
    def Run_Simulation(self,initial_frame,value_loop,ms_value):
        """
        Starts or stops the simulation when the button is clicked.
        """
        # Check if the timer is already running Use hasattr(self, 'timer') to ensure the self.timer attribute exists before calling isActive().
        if hasattr(self, 'timer') and self.timer.isActive():
            # Stop the timer if it's running
            self.timer.stop()
            self.iteration = initial_frame  # Reset the iteration counter
            print("Simulation stopped.")
        else:
            """The timeout signal of QTimer does not pass any arguments 
                when it is emitted. However, the update_simulation method
                  requires two arguments: initial_frame and value_loop. 
                  To bridge this gap, a lambda function is used to wrap 
                  the call to update_simulation and provide the required
                    arguments.The lambda creates an anonymous function that
                      calls self.update_simulation(initial_frame, value_loop) 
                      whenever the timeout signal is emitted.

            """
            # Initialize iteration counter
            self.iteration = initial_frame  # Current iteration
            # Set up a timer to update the plot
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: self.update_simulation(initial_frame, value_loop))
            self.timer.start(ms_value)  # Update at the specified interval
            print("Simulation started.")
    add_iteration_txt=Signal(str)
    def update_simulation(self,initial_frame,value_loop):
        if self.iteration<value_loop:
            self.iteration= self.iteration +1 #we add one to the the iteration of the dinamic graph
            self.next_frame_signal.emit(self.iteration)
            self.add_iteration_txt.emit(f"current iteration: ({self.iteration})")
        else: 
            self.timer.stop()

            self.iteration = initial_frame
            print("Simulation Stopped")
            self.next_frame_signal.emit(self.iteration)
            self.add_iteration_txt.emit(f"current iteration: ()")
    

    ####### CLEARING GUI #########
    def Clearing_Gui(self):
        self.added_channel_tags= [] 
        self.channels = []
        self.channel_labels = [] 
        self.Delays_channel = [] 
        self.Experiment_Hub=[] 
        self.Max_end_time =0 
        self.dev = 'Dev1' 
        self.counter_pin = 'ctr0' 
        self.gate_pin = 'PFI9'



        
        

            



            
                    





    
