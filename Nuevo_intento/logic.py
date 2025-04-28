from Channel_class import Channel
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

class PulseManagerLogic:

    def __init__(self, parent=None):
        super(PulseManagerLogic, self).__init__()
        self.parent = parent  # Store the parent widget):
        self.added_channel_tags= [] # This is the list of the tags of the channels that are added to the database, used to be seld.added_channels
        self.channels = [] # alist with all the createdi instances of the channels
        self.channel_labels = [] # Find a way to get rid of these extra variables
        self.Delays_channel = [] # Find a way to get rid of these extra variables
    adding_flag_to_list=Signal(str)
    def add_channel(self, channel_tag, channel_delay,channel_label): # Only function is to add the channel to the database if the conditions are met, it communicates with the GUI
        """
        Adds a channel to the database.
        """
        # Logic to add a channel to the database
        channel_tag=int(channel_tag)
        if channel_tag not in self.added_channel_tags:  # Check if channel is already added, #flag[0]
            #  This is for the Graphs in the Sequence Plot
            if channel_label=="green" or channel_label=="yellow" or channel_label=="red" or channel_label=="apd" or channel_label=="microwave":
                Label_recognized=True
                
            else: 
                Label_recognized=False
                dlg = QMessageBox(self.parent)
                dlg.setWindowTitle("Error!")
                dlg.setText(f"Label not Recognized, must be either Green, Yellow, Red, Apd, or Microwave")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.exec_()

            if Label_recognized==True:
                flag= [channel_tag,channel_delay,channel_label]
                flag_str = f"channel: {flag[0]}, delay_on: {abs(flag[1][0])}, delay_off: {abs(flag[1][1])}, {flag[2]}"  # Convert list to string
                self.adding_flag_to_list.emit(flag_str) #emit the signal to the GUI

                self.added_channel_tags.append(flag[0]) #add channel to the set
                self.channel_labels.append([flag[0],flag[3]]) ##[[channel, label],[channel, label]] this will be used in update sequence and in remove channel
                self.Delays_channel.append([flag[0],[flag[1][0],flag[1][1]]])
                channel = Channel(channel_tag, channel_label, channel_delay)
                self.channels.append(channel) 

                #  This is for the Add_Pulse function, to check if pb_pulses is empty, and the the channels accrodingly
                """if self.pb_pulses==[]: 
                    for i in range(len(self.added_channels)):
                        self.pb_pulses.append([self.added_channels[i]]) # we add the current channel_list, we should update it 
                        self.Sequence_Pulses.append([self.added_channels[i]])
                        self.Channel_Pulse_iter.append([self.added_channels[i]])
                        self.Max_end_type.append([self.added_channels[i]])
                        self.iteration_list_saving.append([self.added_channels[i]])
                        self.Iteration_All.append([self.added_channels[i]])
                        self.Iteration_All_PB.append([self.added_channels[i]])
                        self.Max_end_no_iter.append([self.added_channels[i]])
                #else: #to update the lists when there is a new channel added to the added chanels list
                self.pb_pulses.append([flag[0]])
                self.Sequence_Pulses.append([flag[0]])
                self.Channel_Pulse_iter.append([flag[0]])
                self.Max_end_type.append([flag[0]])
                self.iteration_list_saving.append([flag[0]])
                self.Iteration_All.append([flag[0]])
                self.Iteration_All_PB.append([flag[0]])
                self.Max_end_no_iter.append([flag[0]])
                #print(f"iteration_list_saving:{self.iteration_list_saving}")"""
        else: 
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText(f"Channel {flag[0]} already added")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        return flag



    def add_pulse_to_channel(self, channel_tag, pulse_delay, pulse_width, pulse_tag):
        """
        Adds a pulse to a channel.
        """
        # Logic to add a pulse to a channel
        for channel in self.channels:
            if channel.channel_tag == channel_tag:
                channel.add_pulse(pulse_delay, pulse_width, pulse_tag)
                break
