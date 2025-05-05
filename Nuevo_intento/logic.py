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
#import spinapi
#from spinapi import Inst, ON
from PySide2.QtGui import QPen,QColor
import pyqtgraph as pg #para los gráficos de las secuencias
import numpy as np
from PySide2.QtCore import QObject , Signal


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
            class experiment. which we then add"""
        for i in range(0,value_loop): #we iterate per each iteration of the experiment
            Exp_i_pb=[]
            for channel in self.channels:
                list_channel_sequence=channel.a_experiment(i)
                if list_channel_sequence!=None: 
                    Exp_i_pb.append(list_channel_sequence)
            exp=Experiment(Exp_i_pb,i)
            exp.Run_Exp()
            self.Experiment_Hub.append(exp)  #since we are going from 0-end loop the exp objects will be ordered
            



            
                    





    
