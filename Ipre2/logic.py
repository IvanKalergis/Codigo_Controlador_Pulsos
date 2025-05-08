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
        self.Max_end_time =0 # It gives you the max end time of all iterations

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
            if channel_label in ["green", "yellow", "red", "apd", "microwave"]:
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

        self.Send_to_Pulse_Blaster(Flat_exp)
        """"
        Here we should add a fucntion to recieve the photon count
        
        """
        #spinapi.pb_start()
        



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

    def Stop_Experiment(self): 
        """spinapi.pb_stop() #stop de program
        spinapi.pb_close() # close the pusle blaster, becasue when you want to open it again it must be close for this"""
        pass



    # ••••• DISPLAY ••••••••
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
        


        
        

            



            
                    





    
