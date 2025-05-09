from Channel_class import Channel
from experiment import Experiment
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
import spinapi
from spinapi import Inst, ON
from PySide2.QtGui import QPen,QColor
import pyqtgraph as pg #para los gráficos de las secuencias
import numpy as np
from PySide2.QtCore import QObject , Signal
##########################
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

#import spinapi
#from spinapi import Inst, LOOP, CONTINUE, END_LOOP, STOP

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
            #  This is for the Graphs in the Sequence Plot
            if channel_label in ["green", "yellow", "red", "apd", "microwave"]:
                flag_str = f"channel: {flag[0]}, delay_on: {abs(flag[1][0])}, delay_off: {abs(flag[1][1])}, {flag[2]}"  # Convert list to string
                self.adding_flag_to_list.emit(flag_str) #emit the signal to the GUI
                channel_binary=self.convert_to_binary(channel_tag,channel_count)
                print(f"channel_binary:{channel_binary}")
                self.added_channel_tags.append(flag[0]) #add channel to the set
                """self.channel_labels.append([flag[0],flag[2]]) ##[[channel, label],[channel, label]] this will be used in update sequence and in remove channel
                self.Delays_channel.append([flag[0],[flag[1][0],flag[1][1]]])"""
                channel = Channel(channel_tag,channel_binary,channel_label, channel_delay)
                self.channels.append(channel) 
                print(f"channel color: {channel.label}")
                
            else: 
                #print('Emitted')
                self.error_str_signal.emit(f"Label {channel_label} not recognized. Please use one of the following: green, yellow, red, apd, microwave")
        else: 
            self.error_str_signal.emit(f"Channel {flag[0]} already added")

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
    def add_pulse_to_channel(self, start_time, width,function_str, iteration_range,channel_tag,type_change):
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
                    channel.a_sequence(start_time,width,function_str,iteration_range,type_change)
                    channel.error_adding_pulse_channel.connect(self.error_str_signal.emit)
                    break
    


    def Run_experiment(self,value_loop):

        """ here we iterate through each iteration of the loop to find the channels that have a sequence for that iteration 
            then we order the pulses form the channels that have pulses in this iteration. Then we create an object from the  
            class experiment. which we then add to our list Experiment_Hub
        """
        for i in range(0,value_loop): #we iterate per each iteration of the experiment
            Exp_i_pb=[]
            for channel in self.channels:
                list_channel_sequence=channel.a_experiment(i)
                if list_channel_sequence!=None: 
                    Exp_i_pb.append(list_channel_sequence)
            exp=Experiment(Exp_i_pb,i)
            exp.Prepare_Exp()
            self.Experiment_Hub.append(exp)  #since we are going from 0-end loop the exp objects will be ordered
        """ Con la lista Experiment_hub ya completa, flateamos la lista, y luego le enviamos los pulsos a la pulse Blaster """
        # Flatten all the pulses into one list
        Flat_exp= [pulse for exp in self.Experiment_Hub for pulse in exp.pb_sequence]
        ##### Just to check if it's working #######

        self.Send_to_Pulse_Blaster(Flat_exp)

        counter=self.create_counter_task()
        counter.start()
        timeout = (value_loop*10*1.2) #el el timepo total del experimento *1.2
        spinapi.pb_start()
        for channel in self.channels:
            if channel.label=='APD' or channel.label=='apd':
                counts = counter.read(value_loop,timeout=timeout)
                count_0=counts[0]
                counts = np.diff(counts) # instead of accumulating values ex (5,11,21) it gives (5,6,10)
                print(counts)
        



    def Send_to_Pulse_Blaster(self,Flat_exp):
        """
        Here we recieve the flat list with all the pulses, which we then sen to the PB
        """
        spinapi.pb_close()
        spinapi.pb_select_board(0)
        if spinapi.pb_init() != 0:
            #####print("Error initializing board: %s" %pb_get_error())
            input("Please press a key to continue.")
            exit(-1)
        spinapi.pb_reset() 
        spinapi.pb_core_clock(500)
        spinapi.pb_start_programming(spinapi.PULSE_PROGRAM)
        start=spinapi.pb_inst_pbonly(int(sum(Flat_exp[0].channel_binary[0])),Inst.LOOP,1,(Flat_exp[0].end_tail-Flat_exp[0].start_tail)*spinapi.us)
        print(f"Flat_exp[0].channel_binary:{Flat_exp[0].channel_binary[0]}")
        print(f"spinapi.pb_inst_pbonly({sum(Flat_exp[0].channel_binary[0])},Inst.LOOP,{1},({Flat_exp[0].end_tail-Flat_exp[0].start_tail})*spinapi.us)") 
        for i in range(1,len(Flat_exp)):# we start from one because we already did the 0 index
            if i!=len(Flat_exp) -1:
                print(f"spinapi.pb_inst_pbonly({sum(list(Flat_exp[i].channel_binary[0]))},Inst.CONTINUE,0,({Flat_exp[i].end_tail-Flat_exp[i].start_tail})*spinapi.us)")
                spinapi.pb_inst_pbonly(int(sum(Flat_exp[i].channel_binary[0])),Inst.CONTINUE,0,(Flat_exp[i].end_tail-Flat_exp[i].start_tail)*spinapi.us)
            else:
                print(f"spinapi.pb_inst_pbonly({sum(list(Flat_exp[i].channel_binary[0]))},Inst.CONTINUE,0,({Flat_exp[i].end_tail-Flat_exp[i].start_tail})*spinapi.us)")
                spinapi.pb_inst_pbonly(int(sum(Flat_exp[i].channel_binary[0])),Inst.CONTINUE,0,(Flat_exp[i].end_tail-Flat_exp[i].start_tail)*spinapi.us)
                print(f"spinapi.pb_inst_pbonly({sum(list(Flat_exp[i].channel_binary[0]))},Inst.END_LOOP,start,{Flat_exp[i].end_tail-Flat_exp[i].start_tail}")
                spinapi.pb_inst_pbonly(int(sum(Flat_exp[i].channel_binary[0])),Inst.END_LOOP,start,Flat_exp[i].end_tail-Flat_exp[i].start_tail)
        spinapi.pb_inst_pbonly(int(0),Inst.STOP,0,1*spinapi.us) # This instruction stops the pulse sequence. The duration is set to a very small value to ensure the stop instruction is executed almost immediately.
        print(f"spinapi.pb_inst_pbonly(int(0),Inst.STOP,0,0.01*spinapi.us)")
        spinapi.pb_stop_programming()  # This function call signals the end of programming the pulse sequence. It tells the SpinAPI library that the sequence definition is complete and the pulse program can be finalized
        print(f"spinapi.pb_stop_programming()")
        spinapi.pb_reset() 
        
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
        spinapi.pb_stop()
        spinapi.pb_close()

            



            
                    





    
