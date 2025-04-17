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
from Sequence import Ui_Form  # Assuming the UI class is named Ui_MainWindow
from PySide2.QtCore import QObject , Signal
class Logic(QObject):
    #def __init__(self):
    def __init__(self, parent=None):
        super(Logic, self).__init__()
        self.parent = parent  # Store the parent widget
        self.Delays_channel=[] # [[channel,[delay_on,delay_off]],[channel,[delay_on,delay_off]]  ]
        self.added_channels = []  # Set to keep track of added channels
        self.channel_labels=[] #[[channel, label],[channel, label]]
        self.added_flags=[]
        self.pb_pulses=[] # here we keep all the pulses added from all the channels,adjusted for the delays, this is for the pulse blaster
        self.Sequence_Pulses=[] #this is the sequence that will be used for the graph, it shows the intended intervals
        self.green_list=[]
        self.green_list_pb=[]
        self.yellow_list=[]
        self.yellow_list_pb=[]
        self.red_list=[]
        self.red_list_pb=[]
        self.apd_list=[]
        self.apd_list_pb=[]
        self.micro_list=[]
        self.micro_list_pb=[]
        self.final_result=[]
        self.Channel_Pulse_iter=[]# this is only to check for iteration overlap
        self.All_List=[] # [ [channe,[,],[,]], [channle,[,],[,]] ] ordered Pb pulses
        self.Max_end_type=[] #[ [channel,[pulse,[type,max_end]]], [channel,.....]] ### this only save the max end time with iterations
        self.iteration_list_saving=[]
        self.Iteration_All=[] # of intended pulses [[channel, [pulse,[type,[iter],start,[results]]]]], this will be used specifically for the simulation
        self.Start_Results=[]# a list that serves a value holder each time there is a variatin added, to give the values of startn and the result to self.Iteration_ALl
        self.Global_end_time=0#the largest time value for the sequence delayed one element is including the delay, and the other is the time intended by the user, we need to change this to not include the delays
        self.iteration = 0
         ######## for the PBlaster:
        self.Iteration_All_PB=[]#[ [channel,[pulse,[type,start,[iter],results_width],[type,start,[iter],results] ] ]]
        self.All_List_PB=[]
        #######
        self.PULSE_BLASTER=[]
        self.Max_end_no_iter=[] #should be like[ [channel,[pulse,end_time]],[channel,[pulse,end]]]
        pass
    def respect_simulation_Channel(self,delay_on, delay_off,channel,channel_label): #we only allow the addition of the channel once the simulation has already runnes, to avoid errors
        if self.iteration==0:
            self.Add_to_List(delay_on, delay_off,channel,channel_label)
            print("allowed to add a channel")
        else:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText(f"End simulation before adding new channel")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
    sequence_signals=Signal(pg.PlotDataItem)  # Define a Signal that emits the corresponding plot to the gui doc
    adding_list_signal=Signal(str)
    print_stuff=Signal(list)
    def Add_to_List(self,channel,delay_on, delay_off,channel_label): #we add the channels to the list
        channel=int(channel)
        flag=[channel,delay_on,delay_off,channel_label]
        Label_recognized=True #we assume fisrt that the lable is either green, or yellow or red or ...
        lista=self.added_channels
        if channel not in lista:  # Check if channel is already added, #flag[0]
            #  This is for the Graphs in the Sequence Plot
            if channel_label=="green":
                self.green_sequence = pg.PlotDataItem( [0, 100, 200, 300],[5, 5, 5, 5], pen={'color': (44, 160, 44), 'width': 1.5})
                self.sequence_signals.emit(self.green_sequence)
                #self.ui.Sequence_Diagram.addItem(self.green_sequence)
                pass
            elif channel_label=="yellow":
                self.yellow_sequence = pg.PlotDataItem([0, 100, 200, 300], [15, 15, 15, 15], pen={'color': (254, 198, 21), 'width': 1.5})
                self.sequence_signals.emit(self.yellow_sequence)
                #self.ui.Sequence_Diagram.addItem(self.yellow_sequence)
                pass
            elif channel_label=="red":
                self.red_sequence = pg.PlotDataItem([0, 100, 200, 300], [25, 25, 25, 25], pen={'color': (214, 39, 40), 'width': 1.5})
                self.sequence_signals.emit(self.red_sequence)
                #self.ui.Sequence_Diagram.addItem(self.red_sequence)
                pass
            elif channel_label=="apd":
                self.apd_sequence = pg.PlotDataItem([0, 100, 200, 300], [35, 35, 35, 35], pen={'color': (250, 250, 250), 'width': 1.5})
                self.sequence_signals.emit(self.apd_sequence)
                #self.ui.Sequence_Diagram.addItem(self.apd_sequence)
                pass
            elif channel_label=="microwave":
                self.micro_sequence = pg.PlotDataItem([0, 100, 200, 300], [45, 45, 45, 45], pen={'color': (128, 0, 128), 'width': 1.5})
                self.sequence_signals.emit(self.micro_sequence)
                #self.ui.Sequence_Diagram.addItem(self.micro_sequence)
                pass
            else: 
                Label_recognized=False
                dlg = QMessageBox(self.parent)
                dlg.setWindowTitle("Error!")
                dlg.setText(f"Label not Recognized, must be either Green, Yellow, Red, Apd, or Microwave")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.exec_()

            if Label_recognized==True:
                flag_str = f"channel: {flag[0]}, delay_on: {abs(flag[1])}, delay_off: {abs(flag[2])}, {flag[3]}"  # Convert list to string
                self.adding_list_signal.emit(flag_str)
                #self.ui.Channel_List.addItem(flag_str) #we add the chanel with its protpertie to the list
                self.added_channels.append(flag[0]) #add channel to the set
                self.channel_labels.append([flag[0],flag[3]]) ##[[channel, label],[channel, label]] this will be used in update sequence and in remove channel
                self.added_flags.append(flag)
                self.Delays_channel.append([flag[0],[flag[1],flag[2]]])
            
                #  This is for the Add_Pulse function, to check if pb_pulses is empty, and the the channels accrodingly
                if self.pb_pulses==[]: 
                    for i in range(len(self.added_channels)):
                        self.pb_pulses.append([self.added_channels[i]]) # we add the current channel_list, we should update it 
                        self.Sequence_Pulses.append([self.added_channels[i]])
                        self.Channel_Pulse_iter.append([self.added_channels[i]])
                        self.Max_end_type.append([self.added_channels[i]])
                        self.iteration_list_saving.append([self.added_channels[i]])
                        self.Iteration_All.append([self.added_channels[i]])
                        self.Iteration_All_PB.append([self.added_channels[i]])
                        self.Max_end_no_iter.append([self.added_channels[i]])
                else: #to update the lists when there is a new channel added to the added chanels list
                    self.pb_pulses.append([flag[0]])
                    self.Sequence_Pulses.append([flag[0]])
                    self.Channel_Pulse_iter.append([flag[0]])
                    self.Max_end_type.append([flag[0]])
                    self.iteration_list_saving.append([flag[0]])
                    self.Iteration_All.append([flag[0]])
                    self.Iteration_All_PB.append([flag[0]])
                    self.Max_end_no_iter.append([flag[0]])
                    #print(f"iteration_list_saving:{self.iteration_list_saving}")
        else: 
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText(f"Channel {flag[0]} already added")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        return flag





    def respect_simulation_Pulses(self,channel,start_time,width,max_counter): #we only allow the addition of the pulse once the simulation has already runnes, to avoid errors
        if self.iteration==0:
            #print("allowed to add a pulse")
            self.Added_Pulses(channel,start_time,width)
            self.calculate_Loop_Duration(max_counter)
            #print(f"duration:{self.duration}")
        else:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText(f"End simulation before adding a new pulse")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
            #print(f"All_List: {self.All_List)}")
            #print(f"max_end_type: {self.Max_end_type}")
            #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
            #print(f"max_end_no_iter:{self.Max_end_no_iter}")

    def respect_simulation_Change_Pulse(self,pulse_flag,pulse_box_count,channel_index_box,current_pulse,max_counter): #we only allow the addition of the channel once the simulation has already runnes, to avoid errors
        if self.iteration==0:
            print("allowed to vary pulse width")
            self.add_varying_pulse_width(pulse_flag,pulse_box_count,channel_index_box,current_pulse)
            self.calculate_Loop_Duration(max_counter)
            print(f"duration:{self.duration}")
        else:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText(f"End simulation before changing pulse width")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        #print(f"All_List: {self.pulses_ordered_by_time_channels()}")
        #print(f"max_end_type: {self.Max_end_type}")
        #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
        #print(f"max_end_no_iter:{self.Max_end_no_iter}")





    
    
    def Added_Pulses(self,channel,start_time,width):
        channel=channel #the value of the channel
        if len(self.added_channels)==0:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText("No channels added")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
            return
        elif channel not in self.added_channels:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText(f"Channel {channel} not added")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        elif channel in self.added_channels:
            #find the delays of the  channel in the added_flags list
            delay_on=0
            delay_off=0
            for i in range(len(self.added_flags)):
                #print(f"Channel_Pulse.currentIndex(): {self.ui.Channel_Pulse.currentIndex()}")
                #here we find the delays of the channel, using the added_flags list and the index which corresponds to th evalue fo the channel
                if self.added_flags[i][0]==channel:
                    delay_on=self.added_flags[i][1]
                    delay_off=self.added_flags[i][2]
                    channel_label=self.added_flags[i][3]     
            #we need to adjust the intervals to account for the delays 
            start_time= start_time
            width= width
            #including the delays
            end_tail=start_time+width-delay_off
            start_tail=start_time-delay_on
            Adjusted_Interval=[start_tail,end_tail] #specifically for the Pulse_Blaster, these are the intervals that account for the delays to maintain the intended timeframes
            #print(f"Adjusted_I: {Adjusted_Interval}")
            pulse_collapse=False
            if delay_off>=width:
                pulse_collapse=True
            overlap_fixed_pulses=False #we define this variable to let the system know when there is an overlap with the fixed pulses
            overlap_variations_pulses=False  #we define this variable to let the system know when there is an overlap with the variations pulses
            if Adjusted_Interval[0]>=0 and pulse_collapse==False: #if the adjustes_interval starts after or on 0=t, to avoid negative time
                Intended_interval=[start_time,start_time+width] #Shown in the graph  
                #delayed_interval= [start_time+delay_on,start_time+width+delay_off] 
                #now we check if its possible account for the delays in the specific channel (checking if there are any other pulses in the same channel, that overlap with these intervals)
                #allows me to not get an error: List index out of range in the first iteration
                Index = self.find_indices_first_terms(self.pb_pulses , int(channel) ) # we get the index of the combobox which is the value of the channel, we find the index of this value on pb_pulses
                #print(f"index: {Index}")
                #print(f"pb_pulses: {len(self.pb_pulses[Index])}")
                if len(self.pb_pulses[Index]) > 1 : #if there are other puslse on the same channel we need to check for overlapping, and we also check if the list on the index has a sublist
                    for j in range(len(self.pb_pulses[Index])): #we iterate over the pb_pulses in the respective channel, to check for overlapping
                        if j>0:
                            Partially_Left=(self.pb_pulses[Index][j][0]<=end_tail and self.pb_pulses[Index][j][0]>=start_tail) # if the the new pulse finishes after the start of the previous pulse and starts before the start of the previous pulse
                            Partially_Right=(self.pb_pulses[Index][j][1]<=end_tail and self.pb_pulses[Index][j][1]>=start_tail) # if the new pulse finishes after the end of the previous pulse and starts before the end of the previous pulse
                            Completely_Inside=(self.pb_pulses[Index][j][0]<=start_tail and self.pb_pulses[Index][j][1]>=end_tail) #if the new pulse starts after the start of the previous pulse and finishes before the end of the previous pulse
                            if Partially_Left==True or Partially_Right==True or Completely_Inside==True: #if the pulse is partially, or completely inside the interval the overlap varible becomes true
                                overlap_fixed_pulses=True 
                    #print(Partially_Left,Partially_Right,Partially_Right)
                    #print(f"overlapped: {overlap_fixed_pulses}")
                    #######################################
                    #now we must check for overlapping with any of the pulses that have variations
                    #only if the variation pulse comes before the new pulse (oteriwse we asumme it is accounted for) and only if the pulse is type=0
                    if overlap_fixed_pulses==False: #we only check for overlapping on varying pulses if there wasnt overlapping on fixed pulses
                        index_max_end_channel=self.find_indices_first_terms(self.Max_end_type, int(channel))
                        if self.contains_sublists(self.Max_end_type)== True: # to check if there are actual variations of iterations in the respective channel
                            self.All_List=self.pulses_ordered_by_time_channels()  
                            self.All_List_PB=self.pulses_ordered_by_time_channels_pb() 
                            #print(f"All_List_PB: {self.All_List_PB}")
                            #print(f"All_List{self.All_List}")
                            #print(f"channel: {channel}")
                            #index_All_list=self.find_indices_first_terms(self.All_List,channel) # is returning a none TYpe
                            index_All_list_pb=self.find_indices_first_terms(self.All_List_PB,channel)
                            #filtered_list=self.All_List[index_All_list]
                            filtered_list_pb=self.All_List_PB[index_All_list_pb]
                            #print(f"filtered_list: {filtered_list}")
                            #print(f"filtered_list_pb: {filtered_list_pb}")
                            #find the pulse that comes before
                            Found_Top=False
                            for j in range(len(filtered_list_pb)):
                                if j>0:
                                    if filtered_list_pb[j][0]<start_tail and filtered_list_pb[j][1]<end_tail and Found_Top==False: #the pulse goes before our new pulse
                                        if len(filtered_list_pb)== j+1 and Found_Top==False: # it reached the end of the filtered list and still all the pulses come before of the new pulse
                                            Found_Top=True
                                            Previous_Pulse=j# the index of the pulse which is previous to the new pulse

                                    elif filtered_list_pb[j][0]>start_tail and filtered_list_pb[j][1]>end_tail and j>1 and Found_Top==False: # the pulse goes after our new pulse, and we make sure that there is another pulse before the new pulse
                                        Found_Top=True
                                        Previous_Pulse=j-1
                                    elif filtered_list_pb[j][0]>start_tail and filtered_list_pb[j][1]>end_tail and j==1 and Found_Top==False: # the first pulse comes after our new pulse, so there is no overlapping
                                        Found_Top=True
                                        Previous_Pulse=None
                            if Found_Top==True: #now we check for overlapping
                                #print(f"Previous_Pulse: {Previous_Pulse}")
                                #print(f"channel:{channel}")
                                #print(f"index_channel:{index_max_end_channel}")
                                if Previous_Pulse!=None:
                                    #print(f"pb_pulses:{self.pb_pulses}")
                                    #print(f"max_end[channel][Previous_Pulse]: {self.Max_end_type}") #[ [channel,[pulse,[type],[max_end]]], [channel,.....]]
                                    for i in range(len(self.Max_end_type[index_max_end_channel][Previous_Pulse])):  #list out of range
                                        if i>0:
                                            if len(self.Max_end_type[index_max_end_channel][Previous_Pulse])>1:
                                                #print(f"i:{i}")
                                                #print(f"max_end[channel][Previous_Pulse]: {self.Max_end_type[channel][Previous_Pulse]}")
                                                if self.Max_end_type[index_max_end_channel][Previous_Pulse][i][1]>start_tail:
                                                    overlap_variations_pulses=True
    
                    if overlap_fixed_pulses==True: 
                        dlg = QMessageBox(self.parent)
                        dlg.setWindowTitle("Error!")
                        dlg.setText(f"Overlapping pulses in channel {channel}")
                        dlg.setStandardButtons(QMessageBox.Ok)
                        dlg.exec_() 
                    elif overlap_variations_pulses==True:
                        dlg = QMessageBox(self.parent)
                        dlg.setWindowTitle("Error!")
                        dlg.setText(f"Overlapping pulses in channel {channel}, due to the increasing iteration on pulse: {Previous_Pulse}")
                        dlg.setStandardButtons(QMessageBox.Ok)
                        dlg.exec_() 
                    else:
                        #print("No overlapping pulses2")
                        self.pb_pulses[Index].append(Adjusted_Interval) #we add the adjusted intervals to the sequence, this is for the pulse blaster
                        self.Sequence_Pulses[Index].append(Intended_interval)#we add the intended intervals to the sequence    
                        self.update_graph_sequence() # this allows us to update the sequence in the graph
                        #print(f"All_list: {self.All_List}")
                        #print(f"All_list_pb_inside: {self.All_List_PB}")
                        if self.Global_end_time<Adjusted_Interval[1]:
                            self.Global_end_time=Adjusted_Interval[1]
                        self.All_List=self.pulses_ordered_by_time_channels() 
                        self.All_List_PB=self.pulses_ordered_by_time_channels_pb()
                        #print(f"All_list: {self.All_List}")
                        All_index_channel_pb=self.find_indices_first_terms(self.All_List_PB,channel)
                        Pulse=self.All_List_PB[All_index_channel_pb].index(Adjusted_Interval)
                        #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
                        #see if there are other pulses infront of this new pulse
                        #print(f"channel=channel_iter: {self.Channel_Pulse_iter[Index][0]==channel}")
                        #print(f"Adjusted_Interval: {Adjusted_Interval}")
                        #print(f"self.All_List[index]: {self.All_List[All_index_channel]}")
                        #print(f"len(self.All_List[index]): {len(self.All_List[All_index_channel])}")
                        #print(f"channel=iteration_List: {self.iteration_list_saving[Index][0]==channel}")
                        #print(f"ALl_index_channel: {All_index_channel}")
                        #print(f"Pulse:{Pulse}")
                        #we need to add the pulse number to the self.Channel_Pulse_iter
                        if len(self.Channel_Pulse_iter[Index])==1:
                            self.Channel_Pulse_iter[Index].append([1]) #this one simbolizes a pulse_1 we get = [ [channel,[1]] ]
                            self.Max_end_type[Index].append([1],Intended_interval[1])
                            self.Max_end_no_iter[Index].append([1])
                            #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
                            #####################
                            #if we add a pulse in between 2 pulses
                            #lets say i have two pulses and i place one in between, since the Pulse_Box keeps the time order the 2nd pulse will become the new pulse (will this pulse steal the variations from the now 3rd pulse)?Iteration List keeps the second pulse:
                        elif Pulse<len(self.All_List_PB[All_index_channel_pb])-1: #here we check if there is pulse after the new pulse, the -1 is to substrac the channel element
                            Pulses_to_update= list(range(Pulse,len(self.All_List_PB[All_index_channel_pb]))) # a list with the pulses to update, it was Pulse+1 before
                            #print("there are other pulses infront")
                            #print(f"  Pulse:{Pulse}")
                            #print(f"  Pulses to Update:{Pulses_to_update} ")
                            #if there are, update the variables we add the the new pulse to its position, so all the pulses infront get displaced +1
                            self.Channel_Pulse_iter[Index].insert(Pulse,[Pulse])
                            self.Max_end_type[Index].insert(Pulse,[Pulse])
                            self.Max_end_no_iter[Index].insert(Pulse,[Pulse])
                            self.Iteration_All[Index].insert(Pulse,[Pulse])
                            self.Iteration_All_PB[Index].insert(Pulse,[Pulse])######
                            #print(f"Iteration_ALl_pb:{self.Iteration_All_PB}")
                           # print(f"Iteration_ALl:{self.Iteration_All}")
                            #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
                            #print(f"Max_end_type:{self.Max_end_type}")
                            for i in range(len(Pulses_to_update)):######## its giving me out of range because the pulses are dispaced to the right
                                print(f"i:{i}")
                                self.Channel_Pulse_iter[Index][Pulses_to_update[i]][0]=Pulses_to_update[i]#this changees the value of the following pulses
                                self.Max_end_type[Index][Pulses_to_update[i]][0]=Pulses_to_update[i]
                                self.Max_end_no_iter[Index][Pulses_to_update[i]][0]=Pulses_to_update[i]
                                self.Iteration_All[Index][Pulses_to_update[i]][0]=Pulses_to_update[i]
                                self.Iteration_All_PB[Index][Pulses_to_update[i]][0]=Pulses_to_update[i]
                                print(f"Iteration_ALl_pb:{self.Iteration_All_PB}")
                                print(f"Iteration_ALl:{self.Iteration_All}")
                                #we need to order the 
                            #print(f"Iteration_ALl:{self.Iteration_All}")

                                
                            #for self.iteration_list_saving we must only update the pulse that get displaced not add a new pulse
                            for j in range(len(self.iteration_list_saving[Index])): # we go about the len of the list -1 which corresponds to the channel
                                if j>0:
                                    # Snce each elelemtn is like this 'Pulse:2, type: 0, function: W*i , iteration range: [0, 1]', we need to extract the pulse number
                                    #print(f"iteration_list_saving:{self.iteration_list_saving[Index][j][0]}")
                                    element_string = self.iteration_list_saving[Index][j][0]  # Access the string element within the list
                                    update_value = int(element_string.split(",")[0].split(":")[1].strip()) +1 # we add 1 because the pulse that was previosly n now is n+1, were n is the order of the new pulse
                                    #print(f" value_list_Pulse: { update_value}")
                                    #print(f"Pulse:{Pulse}")
                                    if Pulse<update_value: #we chech if the new pulse is less than one of the pulses from the list
                                        #now we join the values again, with the updated value
                                        parts = element_string.split(",")
                                        parts[0] = ":".join([parts[0].split(":")[0], f"{update_value}"])  # Modify and join in one line
                                        # Join the parts back together
                                        new_string = ",".join(parts) # here we have the new value for the index of the list
                                        self.iteration_list_saving[Index][j][0]=new_string
                                        #self.show_varying_pulses()
                            #print(f"iteration_list_saving:{self.iteration_list_saving}")
                        else:
                            index_previous=len(self.Channel_Pulse_iter[Index])-1 # here we get the index of the last pulse on the list Channel_Pulse_iter
                            previous=self.Channel_Pulse_iter[Index][index_previous][0] # we save the previous pulse number
                            actual_pulse= previous + 1
                            self.Channel_Pulse_iter[Index].append([actual_pulse]) #here we add the actual pulse number to the list
                            self.Max_end_type[Index].append([actual_pulse])
                            self.Max_end_no_iter[Index].append([actual_pulse,Intended_interval[1]])
                            self.Iteration_All[Index].append([actual_pulse])
                            self.Iteration_All_PB[Index].append([actual_pulse])

                else: #there are no other pulses on this channel
                    #print("No overlapping pulses1")
                    self.pb_pulses[Index].append(Adjusted_Interval) #we add the adjusted intervals to the sequence, this is for the pulse blaster
                    self.Sequence_Pulses[Index].append(Intended_interval)#we add the intended intervals to the sequence    
                    self.update_graph_sequence() # this allows us to update the sequence in the graph
                    self.All_List=self.pulses_ordered_by_time_channels()  
                    self.All_List_PB=self.pulses_ordered_by_time_channels_pb()
                    if self.Global_end_time<Adjusted_Interval[1]:
                        self.Global_end_time=Adjusted_Interval[1]
                    #self.iteration_list_saving=[]
                    #we need to add the pulse number to the self.Channel_Pulse_iter
                    if len(self.Channel_Pulse_iter[Index])==1:
                            self.Channel_Pulse_iter[Index].append([1]) #this one simbolizes a pulse_1 we get = [ [channel,[1]] ]
                            self.Max_end_type[Index].append([1])
                            self.Max_end_no_iter[Index].append([1,Intended_interval[1]])
                            self.Iteration_All[Index].append([1])
                            self.Iteration_All_PB[Index].append([1])
                            #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
                    else:
                        index_previous=len(self.Channel_Pulse_iter[Index])-1 # here we get the index of the last pulse on the list Channel_Pulse_iter
                        previous=self.Channel_Pulse_iter[Index][index_previous][0] # we save the previous pulse number
                        actual_pulse= previous + 1
                        self.Channel_Pulse_iter[Index].append([actual_pulse]) #here we add the actual pulse number to the list
                        self.Max_end_type[Index].append([actual_pulse])
                        self.Max_end_no_iter[Index].append([actual_pulse,Intended_interval])
                        self.Iteration_All[Index].append([actual_pulse])
                        self.Iteration_All_PB[Index].append([actual_pulse])
                        #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")

            elif Adjusted_Interval[0]<0: #if runned the interval fails to start after cero, and gives negative time which is not allowed
                dlg = QMessageBox(self.parent)
                dlg.setWindowTitle("Error!")
                dlg.setText(f"Adjusting for the delay, gives negative start_time of {Adjusted_Interval[0]} ")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.exec_()
            else:
                dlg = QMessageBox(self.parent)
                dlg.setWindowTitle("Error!")
                dlg.setText(f"cannot adjust for the delay because width={width}<={delay_off}=delay_off")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.exec_()             
        
        #print(f"All_List: {self.All_List}")
        #print(f"All_List_PB: {self.All_List_PB}")
        #print(f"max_end_type: {self.Max_end_type}")
        #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
        #print(f"max_end_no_iter:{self.Max_end_no_iter}")
        #print(f"Iteration_ALl: {self.Iteration_All}")
        #print(f"Iteration_ALl_PB: {self.Iteration_All_PB}")
        #print(f"Global end t: {self.Global_end_time}")
        #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
        #print(f"Max_end_type:{self.Max_end_type}")
        #print(f"Sequence_Pulses: {self.Sequence_Pulses}")
        #print(f"pb_pulses: {self.pb_pulses}")    
        return [self.pb_pulses] # this is the sequence that will be used for the pulse blaster




    clearing_graph_signal=Signal()
    sequence_signals=Signal(pg.PlotDataItem) 
    def update_graph_sequence(self): # each time we add a pulse, the sequence on the  gets updated on 
        self.clearing_graph_signal.emit() #we send the signal to the gui doc to clear the graph
        #self.ui.Sequence_Diagram.clear() # to reset to cero 
        All_labels=[] #a list that will keep all labels which have a pulse
        self.green_list=[] #the pulse intervals of the green laser
        self.yellow_list=[]
        self.red_list=[]
        self.apd_list=[]
        self.micro_list=[]
        max_end_time=0 # for the bigest x=time value from al the pulses in all the channels, this will ahve to be the max end value for all items in the graph
        #print(f"Sequence_Pulses: {self.Sequence_Pulses}")
        for i in range(len(self.Sequence_Pulses)):
            Index= self.find_indices_first_terms(self.channel_labels, self.Sequence_Pulses[i][0] ) #we find the index of the channel on Sequence_pulses on the channel_labels list
            #now we can addres the label
            label=self.channel_labels[Index][1] #here we save the label 
            if len(self.Sequence_Pulses[i])>1:#here we filter the channels that only have pulses on All_labels
                All_labels.append(label)
            #print(f"label: {label.lower()}")
            #print(f"all_label:{ All_labels } ")
            for j in range(len(self.Sequence_Pulses[i])):
                #print(f"j: {j}")
                if j>0:
                    #  add the new pulses to each corresponding list (channel_list)
                    if label.lower()=="green":
                        #first we define the arrays for the intended pulses
                        self.green_list.append(self.Sequence_Pulses[i][j]) #we add the interval per channel in our list
                        green_ordered=sorted(self.green_list, key=lambda x: x[0]) #order the intervals in time from first to last 
                        green_ordered_int = [[int(x) for x in sublist] for sublist in green_ordered] # to transfrom the float elements into integers
                        #print(f"green_list: {self.green_list}")
                        #print(f"green_ordered_int: {green_ordered_int}")
                        #NOW we do it for the pb pulses.
                        self.green_list_pb.append(self.pb_pulses[i][j])
                        green_ordered_pb=sorted(self.green_list_pb, key=lambda x: x[0]) 
                        green_ordered_int_pb = [[int(x) for x in sublist] for sublist in green_ordered_pb]
                        
                        pass
                    elif label.lower()=="yellow":
                        self.yellow_list.append(self.Sequence_Pulses[i][j])
                        yellow_ordered=sorted(self.yellow_list, key=lambda x: x[0]) 
                        yellow_ordered_int= [[int(x) for x in sublist] for sublist in yellow_ordered]
                        #print(f"Yellow_ordered 1 :{ yellow_ordered_int} ")
                        self.yellow_list_pb.append(self.pb_pulses[i][j])
                        yellow_ordered_pb=sorted(self.yellow_list_pb, key=lambda x: x[0]) 
                        yellow_ordered_int_pb = [[int(x) for x in sublist] for sublist in yellow_ordered_pb]                     
                        pass
                    elif label.lower()=="red":
                        self.red_list.append(self.Sequence_Pulses[i][j])
                        red_ordered=sorted(self.red_list, key=lambda x: x[0]) 
                        red_ordered_int=[[int(x) for x in sublist] for sublist in red_ordered]
                        self.red_list_pb.append(self.pb_pulses[i][j])
                        red_ordered_pb=sorted(self.red_list_pb, key=lambda x: x[0]) 
                        red_ordered_int_pb = [[int(x) for x in sublist] for sublist in red_ordered_pb]
                        pass
                    elif label.lower()=="apd":
                        self.apd_list.append(self.Sequence_Pulses[i][j])
                        apd_ordered=sorted(self.apd_list, key=lambda x: x[0]) 
                        apd_ordered_int=[[int(x) for x in sublist] for sublist in apd_ordered]
                        self.apd_list_pb.append(self.pb_pulses[i][j])
                        apd_ordered_pb=sorted(self.apd_list_pb, key=lambda x: x[0]) 
                        apd_ordered_int_pb = [[int(x) for x in sublist] for sublist in apd_ordered_pb]
                        pass
                    elif label.lower()=="microwave":
                        self.micro_list.append(self.Sequence_Pulses[i][j])
                        micro_ordered=sorted(self.micro_list, key=lambda x: x[0])
                        micro_ordered_int=[[int(x) for x in sublist] for sublist in micro_ordered]
                        self.micro_list_pb.append(self.pb_pulses[i][j])
                        micro_ordered_pb=sorted(self.micro_list_pb, key=lambda x: x[0]) 
                        micro_ordered_int_pb = [[int(x) for x in sublist] for sublist in green_ordered_pb]
                        pass  
                    if max_end_time<self.Sequence_Pulses[i][j][1]: # if we find the max end time of between all the pulses to make alll the channels end in the same time in the graph 
                        max_end_time=self.Sequence_Pulses[i][j][1]
                        #print(f"max: {max_end_time}")
        for item in All_labels:
            if "green"==item.lower():
                #we add the signals to the pulse blaster at the graph
                # Create a dashed pen for the pb pulses
                y_green_pb=np.array([ 10 if any(start <= x < end for start, end in green_ordered_int_pb) else 5 for x in np.arange(0, max_end_time, 1)]) 
                x_green_pb=np.linspace(0, max_end_time, len(y_green_pb) + 1)
                self.green_sequence_pb = pg.PlotDataItem(x_green_pb, y_green_pb, stepMode='center', pen={'color':(80, 80, 80),'width': 1.5})  # stepMode allows us to graph with vertical lines
                self.sequence_signals.emit(self.green_sequence_pb)
                #self.ui.Sequence_Diagram.addItem(self.green_sequence_pb)
                #we add the intended values at the graph
                y_green=np.array([ 10 if any(start <= x < end for start, end in green_ordered_int) else 5 for x in np.arange(0, max_end_time, 1)]) 
                x_green=np.linspace(0, max_end_time, len(y_green) + 1)# when using stepMode='center' in pyqtgraph, the length of the x array must be equal to the length of the y array plus one. This requirement ensures that each step has a starting and ending x-coordinate.
                self.green_sequence = pg.PlotDataItem(x_green, y_green, stepMode='center',pen={'color': (44, 160, 44), 'width': 1.5}) # stepmpde allows us to graph with vertical lines
                self.sequence_signals.emit(self.green_sequence)
                #self.ui.Sequence_Diagram.addItem(self.green_sequence)
                #print(f"ygreen={y_green}")
                #print(f"ygreen={y_green}")
            elif "yellow"==item.lower():
                y_yellow_pb=np.array([ 20 if any(start <= x < end for start, end in yellow_ordered_int_pb) else 15 for x in np.arange(0, max_end_time, 1)]) 
                x_yellow_pb=np.linspace(0, max_end_time, len(y_yellow_pb) + 1)
                self.yellow_sequence_pb = pg.PlotDataItem(x_yellow_pb, y_yellow_pb, stepMode='center',pen={'color':(80, 80, 80),'width': 1.5})  # stepMode allows us to graph with vertical lines
                self.sequence_signals.emit(self.yellow_sequence_pb)
                #self.ui.Sequence_Diagram.addItem(self.yellow_sequence_pb)
                y_yellow=np.array([ 20 if any(start <= x < end for start, end in yellow_ordered_int) else 15 for x in np.arange(0, max_end_time, 1)])
                x_yellow=np.linspace(0, max_end_time, len(y_yellow) + 1)
                self.yellow_sequence = pg.PlotDataItem(x_yellow, y_yellow, stepMode='center',pen={'color': (254, 198, 21), 'width': 1.5})
                self.sequence_signals.emit(self.yellow_sequence)
                #self.ui.Sequence_Diagram.addItem(self.yellow_sequence)
                #print("yellow ordered int 2")
                #print(f"y_yellow: {y_yellow}")
                #print(f"x_yellow {x_yellow}")
 
            elif "red"==item.lower():
                y_red_pb=np.array([ 30 if any(start <= x < end for start, end in red_ordered_int_pb) else 25 for x in np.arange(0, max_end_time, 1)]) 
                x_red_pb=np.linspace(0, max_end_time, len(y_red_pb) + 1)
                self.red_sequence_pb = pg.PlotDataItem(x_red_pb, y_red_pb, stepMode='center', pen={'color':(80, 80, 80),'width': 1.5})  # stepMode allows us to graph with vertical lines
                self.sequence_signals.emit(self.red_sequence_pb)
                #self.ui.Sequence_Diagram.addItem(self.red_sequence_pb)
                y_red=np.array([ 30 if any(start <= x < end for start, end in red_ordered_int) else 25 for x in np.arange(0, max_end_time, 1)])
                x_red=np.linspace(0, max_end_time, len(y_red) + 1)
                self.red_sequence = pg.PlotDataItem(x_red, y_red,stepMode='center', pen={'color': (214, 39, 40), 'width': 1.5})
                self.sequence_signals.emit(self.red_sequence)
                #self.ui.Sequence_Diagram.addItem(self.red_sequence)

            elif "apd"== item.lower():
                y_apd_pb=np.array([ 40 if any(start <= x < end for start, end in apd_ordered_int_pb) else 35 for x in np.arange(0, max_end_time, 1)]) 
                x_apd_pb=np.linspace(0, max_end_time, len(y_apd_pb) + 1)
                self.apd_sequence_pb = pg.PlotDataItem(x_apd_pb, y_apd_pb, stepMode='center', pen={'color':(80, 80, 80),'width': 1.5})  # stepMode allows us to graph with vertical lines
                self.sequence_signals.emit(self.apd_sequence_pb)
                #self.ui.Sequence_Diagram.addItem(self.apd_sequence_pb)
                y_apd=np.array([ 40 if any(start <= x < end for start, end in apd_ordered_int) else 35 for x in np.arange(0, max_end_time, 1)])
                x_apd=np.linspace(0, max_end_time, len(y_apd) + 1)
                self.apd_sequence = pg.PlotDataItem(x_apd, y_apd, stepMode='center', pen={'color': (250, 250, 250), 'width': 1.5})
                self.sequence_signals.emit(self.apd_sequence)
                #self.ui.Sequence_Diagram.addItem(self.apd_sequence)

            elif "microwave" ==item.lower():
                y_micro_pb=np.array([ 50 if any(start <= x < end for start, end in micro_ordered_int_pb) else 45 for x in np.arange(0, max_end_time, 1)]) 
                x_micro_pb=np.linspace(0, max_end_time, len(y_micro_pb) + 1)
                self.micro_sequence_pb = pg.PlotDataItem(x_micro_pb, y_micro_pb, stepMode='center', pen={'color':(80, 80, 80),'width': 1.5})  # stepMode allows us to graph with vertical lines
                self.sequence_signals.emit(self.micro_sequence_pb)
                #self.ui.Sequence_Diagram.addItem(self.micro_sequence_pb)
                y_micro=np.array([ 50 if any(start <= x < end for start, end in micro_ordered_int)else 45 for x in np.arange(0, max_end_time, 1)])
                x_micro=np.linspace(0, max_end_time, len(y_micro) + 1)
                self.micro_sequence = pg.PlotDataItem(x_micro, y_micro,stepMode='center', pen={'color': (128, 0, 128), 'width': 1.5})
                self.sequence_signals.emit(self.micro_sequence)
                #self.ui.Sequence_Diagram.addItem(self.micro_sequence)
        
    






    Pulse_i=Signal(str)
    iteration_j=Signal(str)
    def show_varying_pulses(self, channel_pulse_index): #when we change the channel on our self.ui.Channel.Pulse, we get our pulses per channel in our pUlses_Box
        #self.ui.Pulses_box.clear() #as soon as the Channel_box changes the pulse box is cleared and add the pulses for the respective. 
        #self.ui.Iteration_list.clear()
        if self.Sequence_Pulses!=[]:
            index_respective_pulse=self.find_indices_first_terms(self.Sequence_Pulses, channel_pulse_index)
            if index_respective_pulse!= None: 
                #print(f"current index: {self.ui.Channel_Pulse.currentIndex()}")
                #print(f"index_respective_pulse:{index_respective_pulse}")
                n_pulses=len(self.Sequence_Pulses[index_respective_pulse])-1 #we get the number of pulses by counting the  intervals and discount one because the firs element is the channel, not  an interval 
                if n_pulses>0:
                    PulseBox=[]
                    for i in range(n_pulses):
                        #PulseBox.append(f"Pulse:{i+1}")
                        #self.ui.Pulses_box.addItem(f"Pulse:{i+1}") # we add the pulse to the pulse combobox for the corresponding channels
                        self.Pulse_i.emit(f"Pulse:{i+1}")
                    iteration_list=[]
                    for j in range(len(self.iteration_list_saving[index_respective_pulse])):
                        if len(self.iteration_list_saving[index_respective_pulse])>1:
                            if j>0:
                                #print(f"j: {j}")
                                #print(f"len(Iteration_list)): {len(self.iteration_list_saving[index_respective_pulse])}")
                                #iteration_list.append(str(self.iteration_list_saving[index_respective_pulse][j]))
                                self.iteration_j.emit(str(self.iteration_list_saving[index_respective_pulse][j]))
                                #self.ui.Iteration_list.addItem(str(self.iteration_list_saving[index_respective_pulse][j])) # we add the flags again to the list 
                            pass #print(f"iteration_list_saving:{self.iteration_list_saving}")
        pass

    itera_list=Signal(str)
    def add_varying_pulse_width(self,pulse_flag,pulse_box_count, channel_index_box,current_pulse):
        # we save the pulse, the type, the function, the iteration range
        #print(f" self.ui.Type_Change.currentIndex(): { self.ui.Type_Change.currentIndex()}")
        pulse_flag_str=f"{pulse_flag[0]}, type: {pulse_flag[1]}, function: {pulse_flag[2]}, iteration range: {pulse_flag[3]}"
        if pulse_box_count==0: #meaning the combobox doesnt have pulses, the channel doesnt have  pulses
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText("No pulses added in this channel")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        #lets receive the function
        elif 'i' not in pulse_flag[2] or 'W' not in pulse_flag[2]:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText("Must include these two variables: i and W")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        elif channel_index_box not in self.added_channels:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText(f"Channel {channel_index_box} not added")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        else:
            index_channel_iter=self.find_indices_first_terms(self.Channel_Pulse_iter,channel_index_box) #we get the index of the list were the current channel is
            index_channel=self.find_indices_first_terms(self.All_List_PB,channel_index_box) # we find the index for the channel, and we use All_list because we want our pulses to be ordered by time in our combobox
            #print(f"index_channel: {index_channel}")
            current_pulse=current_pulse + 1 #we add one for the first pulse to start at one and not at 0. this pulses are not ordered in time
            #print(f"current_pulse: {current_pulse}")
            if len(self.Channel_Pulse_iter[index_channel_iter][current_pulse])==1: #[ [channel,[pulse,[iter],[iter]] if the respective pulse has no iter
                #print(f"first iter added to pulse ")
                overlap_iter=False
    
            #overlap of iterations we must call the function (overlapping iterations) (lets say for pulse one i previously added a variation from iteration [5,10], and then I added an iteration from [6,25])
            elif len(self.Channel_Pulse_iter[index_channel_iter][ current_pulse])>1:
                result_iterations= self.Overlapping_iterations(index_channel_iter,pulse_flag,current_pulse)
                if result_iterations[0]==True:#if iterations overlap
                    overlap_iter=True
                    dlg = QMessageBox(self.parent)
                    dlg.setWindowTitle("Error!")
                    dlg.setText(f"Iteration range: {pulse_flag[3]} overlaps with {self.Overlapping_iterations(index_channel_iter,pulse_flag,current_pulse)[1]}")
                    dlg.setStandardButtons(QMessageBox.Ok)
                    dlg.exec_()
                else: #runs if overlapping iterations is False
                    overlap_iter=False
            
            if overlap_iter==False: 
                result=self.Overlapping_Pulses(index_channel,pulse_flag,current_pulse,channel_index_box)
                #print(f"result_pulses:{result}")
                if result[0]==True: #meaning its overlapping
                    dlg = QMessageBox(self.parent)
                    dlg.setWindowTitle("Error!")
                    dlg.setText(f"Pulse overlaps on the {result[1]} iteration")
                    dlg.setStandardButtons(QMessageBox.Ok)
                    dlg.exec_()
                else: 
                    #print("variation pulses dont overlap")
                    self.Channel_Pulse_iter[index_channel_iter][ current_pulse].append(pulse_flag[3]) # we add the iterations to the list [ [channel,[pulse,[iter],[iter]]
                    #self.ui.Iteration_list.addItem(pulse_flag_str)
                    self.itera_list.emit(pulse_flag_str)
                    self.Iteration_All[index_channel_iter][current_pulse].append([pulse_flag[1],self.Start_Results[0],pulse_flag[3],self.Start_Results[1]]) #[ [channel,[pulse,[type,start,[iter],results_widt],[type,start,[iter],results] ] ]]
                    self.Iteration_All_PB[index_channel_iter][current_pulse].append([pulse_flag[1],self.Start_Results_PB[0],pulse_flag[3],self.Start_Results_PB[1]])
                    #print(f"Iteration_All:{ self.Iteration_All}")
                    #print(f"Iteration_All_PB:{ self.Iteration_All_PB}")
                    #now we need to save this on self.iteration_list_saving
                    if self.iteration_list_saving!=[]:
                        for i in range(len(self.iteration_list_saving)):
                            if self.iteration_list_saving[i][0]==channel_index_box:#self.ui.Channel_Pulse.currentIndex()
                                self.iteration_list_saving[i].append([pulse_flag_str])             
            #print(f"iteration_list_saving:{self.iteration_list_saving}")
            #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
            pass
                    
    
            


    def create_function_from_string(self, func_str):
        # A multi-line string that dynamically creates the code for a new function generated_function. #change: used to be for i in i_values
        code = f""" 
def generated_function(i_values, W):
        return [({func_str}) for i in i_values] 
"""
        #An empty dictionary used to safely store the result of executing the dynamic code. It prevents the dynamic execution from polluting the global namespace.
        local_dict = {}
        #exec(): A built-in function that dynamically executes the Python code provided in the string code.
        #{}: An empty dictionary for the global namespace, ensuring that no global variables are affected.
        exec(code, {}, local_dict)  # Execute the code string in a controlled environment
        #This means the code inside the exec statement will not have access to or interfere with the global environment or any existing variables outside this isolated space.
        return local_dict['generated_function'] # Retrieves the generated_function from local_dict.
    

    def Overlapping_iterations(self,index_channel_iter,pulse_flag,current_pulse):
        overlap=False
        start_tail=pulse_flag[3][0]
        end_tail=pulse_flag[3][1]
        range_overlap=None
        #print(f"index: {index_channel} current_pulse: {current_pulse}")
        #print(f"start: {start_tail} end: {end_tail}")
        for j in range(len(self.Channel_Pulse_iter[index_channel_iter][current_pulse])):
            if j>0:
                Partially_Left=(self.Channel_Pulse_iter[index_channel_iter][current_pulse][j][0]<=end_tail and self.Channel_Pulse_iter[index_channel_iter][current_pulse][j][0]>=start_tail) 
                Partially_Right=(self.Channel_Pulse_iter[index_channel_iter][current_pulse][j][1]<=end_tail and self.Channel_Pulse_iter[index_channel_iter][current_pulse][j][1]>=start_tail) 
                Completely_Inside=(self.Channel_Pulse_iter[index_channel_iter][current_pulse][j][0]<=start_tail and self.Channel_Pulse_iter[index_channel_iter][current_pulse][j][1]>=end_tail) 
                if Partially_Left==True or Partially_Right==True or Completely_Inside==True: # is partially, or completely inside the interval the overlap varible becomes true
                    overlap=True
                    range_overlap=self.Channel_Pulse_iter[index_channel_iter][current_pulse][j]
        return [overlap,range_overlap] #it returns True i it overlaps and on which iteration range it does
    

    def Overlapping_Pulses(self,index_channel,pulse_flag,current_pulse,channel_index_box):#here we calculate if the pulses overlap,and with which pulse it overlaps
        result=[False,None]

        #we create a list with the amount of time the function is applied [1,2....N]
        #print(f"start_iter:{self.ui.Iterations_start.value()}")
        #print(f"end_iter:{self.ui.Iterations_end.value()}")
        #print((self.ui.Iterations_end.value() - self.ui.Iterations_start.value()) +1)
        #i_values_for_calculation = list(range(1,(self.ui.Iterations_end.value() - self.ui.Iterations_start.value()) +2)) #+2 is crucial
        i_values_for_calculation = list(range(1,(pulse_flag[3][1] - pulse_flag[3][0]) +2)) #+2 is crucial
        #print(f"i_values: {i_values_for_calculation}")
        # we calculate the original pulse width of the intended and pb pulses by using both indexes
        Sequence_ordered=self.order_specific_Channels_Pulses(self.Sequence_Pulses[index_channel])#####
        #print(f"Sequence_Ordered:{Sequence_ordered}")
        pb_ordered=self.order_specific_Channels_Pulses(self.pb_pulses[index_channel])#####
        #print(f"pb_ordered:{pb_ordered}")
        pulse_width_intended=Sequence_ordered[current_pulse-1][1] - Sequence_ordered[current_pulse-1][0] ####### since sequence ordered aswell as pb ordered dont have the channel, we must -1
        pulse_width_pb=pb_ordered[current_pulse-1][1] - pb_ordered[current_pulse-1][0]######
        #print(f"function= {pulse_flag[2]}")
        #print(f"pulse_width_intended={pulse_width_intended}")
        #rint(f"pulse_width_pb={pulse_width_pb}")
        # now we get the desired result per iteration
        new_width_intended_list= self.create_function_from_string(pulse_flag[2])(i_values_for_calculation, pulse_width_intended )  
        #get the delays per current channel to then add to the iteration all intended to get the iteration all pb
        # the delays wont affect overlapping since they are constant for any pulse
        #this works before we add the delays after the calculation of the results.
        new_width_pb_list =[]
        index_delays=self.find_indices_first_terms(self.Delays_channel,channel_index_box)
        delay_off=self.Delays_channel[index_delays][1][1]
        delay_on=self.Delays_channel[index_delays][1][0]
        #print(f"Delays:{self.Delays_channel[index_delays]}")
        #print(f"Delays:{self.Delays_channel[index_delays][1][1]}")
        #print(index_delays)
        if all(delay_off < width for width in new_width_intended_list): #the width of each iter variaton is less than the delay off for adjusting
            #print("delay_off < width")
            for i in range(len(new_width_intended_list)):
                new_width_pb_list.append(new_width_intended_list[i]-delay_off + delay_on)

            #new_width_pb_list = self.create_function_from_string(pulse_flag[2])(i_values_for_calculation, pulse_width_pb )  
            #print(f"new_width:{new_width_pb_list}")
            #print(f"new_width_intended={new_width_intended_list}")
            end_time_list_intended=[]
            end_time_list_pb=[]
            #now we create a list that calculates the end times of the pulse on each iteration
            for i in range(len(i_values_for_calculation)): 
                end_time_list_intended.append(new_width_intended_list[i]+ Sequence_ordered[current_pulse-1][0])#### -1
                #we use intended because that is the width we are trying to achive and only then we add the delays
                # we use pb-prdered for the start because neither the start intended nor the delay changes
                #we only add the delay off
                end_time_list_pb.append(new_width_pb_list[i]+ pb_ordered[current_pulse-1][0]) 
                #end_time_list_pb.append(new_width_pb_list[i]+ pb_ordered[current_pulse-1][0])#####-1

            #print(f"end_time_list_intended:{end_time_list_intended}")
            #print(f"end_time_list_pb:{end_time_list_pb}")
            if pulse_flag[1]==0: #this will mean its the type: Only Pulses Moves, which is index cero from the combobox
                result= self.Only_Pulse_Moves(end_time_list_pb,index_channel,current_pulse,i_values_for_calculation,pulse_flag,channel_index_box) #we see if there is any overlappping using pb_values
                #below i had it with self.sequence_pulses  beofre
                if result[0]==False:
                    self.Start_Results=[self.All_List[index_channel][current_pulse][0],new_width_intended_list] #just to then update Iteration_all
                    self.Start_Results_PB=[self.All_List_PB[index_channel][current_pulse][0],new_width_pb_list] 
                    #print(f"start_resutls:{self.Start_Results}")
                    #print(f"start_pb:{self.Start_Results_PB}")
                    pass
            elif pulse_flag[1]==1:

                pass
            elif pulse_flag[1]==2:
                pass
        else:
            check=False
            for i in range(len(new_width_intended_list)):
                if new_width_intended_list[i]<=delay_off and check==False:
                    iteration=i+pulse_flag[3][0]
                    width=new_width_intended_list[i]
                    check=True
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText(f"cannot adjust for the delay because width={width}<= {delay_off}=delay_off, in iteration {iteration}")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()             

            #print(f"new_width_pb_list: {new_width_pb_list}")
            #print(f"new_width_intended: {new_width_intended_list}")
            #print(f"end_time_list_pb:{end_time_list_pb}")
            #print(f"max_end: {max(end_time_list_pb)}")
            #print(f"type: {pulse_flag[1]}")
            #print(f"result_pb: {new_width_pb_list}")

        return result

    def Only_Pulse_Moves(self, end_time_list_pb,index_channel,current_pulse,i_values_for_calculation,pulse_flag,channel_index_box):
                #check for overlapping:
                # find the pulse coming after this pulse, for this we use the function order_pb_pulses
                        # compar
        overlap=False
        iteration_limit=None
        result=[overlap,iteration_limit]
        #print(f"order_pb{self.order_pb_pulses()} ")
        reference_pb=self.order_pb_pulses() #just for reference and to avoid list out of range
        #print(f"reference:{reference_pb}")
        #  we must filter for the current channel [ [2,[]],[1,[]],[0,[]],[2,[]]] to [ [2,[]], [2,[]]]
        channel=channel_index_box
        #print(f"channel: {channel}")
        #print(f"index_channel: {index_channel}")
        #here we filter the order_pb_pulses to only have the values of the current channel, it gets complicated when we have tuple[ (channel 1,channel 2), [start, end] ]
        # were both channels have the same pulse, or it can also be an integer of only one [ channel 1, [start, end] ]
        #the line below, check for each sublist item in the list reference, then checks if the the first element of the sublist is an integer or a tupple and if the current channel is inside this element
        filtered_list_pb = [[channel, item[1]] for item in reference_pb if (isinstance(item[0], int) and item[0] == channel) or (isinstance(item[0], tuple) and channel in item[0])]  #filtered list is not graving the 
        #print(f"filter_list:{filtered_list_pb} ") 
        # #current_pulse=self.ui.Pulses_box.currentIndex() + 1 #this pulses are not ordered in time
        this_pulse_pb=self.All_List_PB[index_channel][current_pulse] #we get the pulse start time and end time, [start,end], used to be pb_pulse CHANGE
        #print(f"this pulse: {this_pulse}")
        #print(f"All_list_PB: {self.All_List_PB}")
        index_this_pulse_pb=self.find_index(filtered_list_pb,this_pulse_pb) # we find the index for [start,end] in the ordered list the index we recieve is a tupple (channel_index, pulse_index)
        #print(f"current_pulse: {current_pulse}")
        #print(f"pulse_iterval: {this_pulse_pb}")
        #print(f"index_this_pulse:{index_this_pulse_pb}") 
        #print(f"index_next _pulse:{index_this_pulse_pb[0] +1 }") 
        if current_pulse<len(filtered_list_pb):#  we check if the current pulse has another pulse in front of him, since current_pulse is defined as index +1 and len is from 1, infinity
            next_pulse=filtered_list_pb[index_this_pulse_pb[0] + 1][1] # we find the next pulse [start, end]
            #print(f"next_pulse: {next_pulse}")
            #print(f"end_time_list:{end_time_list_pb}") #why is starting at 2?
            #print(f"values for calculation: {i_values_for_calculation}")
            for j in range(len(i_values_for_calculation)):
                if end_time_list_pb[j]>=next_pulse[0] and overlap==False: #if the end value of the current pulse is bigger than the start value of the next pulse we have an overlap
                    #print(f"end_time_list[j]:{end_time_list_pb[j]}") 
                    #print(f"j:{j}")
                    #print("there is overlapping")
                    overlap=True
                    iteration_limit=j + pulse_flag[3][0] 
                    result=[overlap,iteration_limit]
        #print(f"result pulses:{result}")
        #here we add the max_end and the type_ to our global variable
        if result[0]==False: 
            #print("there is no overlap")
            # must have a max_end time for intended and pb, this will be for intended
            max_end=max(end_time_list_pb)
            self.Max_end_type[index_channel][current_pulse].append([pulse_flag[1],max_end]) 
            #print(f"Max_end_type: {self.Max_end_type}")
            ###this might be trivial:
            if self.Global_end_time<max_end:
                self.Global_end_time=max_end
            #print(f"Global end t: {self.Global_end_time}")
        return result

# in both of the functions below we have 
    def Pulse_to_right(self): # Whatever comes afer the pulse moves to the right

        pass
    def Sequence_to_right(self): # The whole sequence after the pulse moves to the right
        pass

    def run_simulation(self):
        self.simulation()
        self.iteration=0




    #it updates every 
    def simulation(self,value_loop,ms_value): #[[channel, [pulse,[type,[iter],start,[results]]]]] in the simulatio we use intended values
        # Initialize iteration counter
        self.iteration = 0 #current iteration
        self.max_iterations = value_loop # Set the maximum number of iterations
        # Set up a timer to update the plot
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation) #the QTimer will call the update_simulation method at regular intervals specified by the user through the QSpinBox.
        self.timer.start(ms_value)  # Update every 100 milliseconds
    
    clear_simulation_graph=Signal()
    add_iteration_txt=Signal(str)
    add_simulation_graph=Signal(pg.PlotDataItem)
    def update_simulation(self):#[[channel, [pulse,[type,start,[iter],[results]]]]]
        print(f"sequence_pulses: {self.Sequence_Pulses}")
        print(f"self.iteration_all: {self.Iteration_All}")
        #print(f"self.Iteration_All: {self.Iteration_All}")
        #self.ui.Simulation.clear()
        self.clear_simulation_graph.emit()
        # Initialize data
        All_labels=[]
        self.green_list=[] #the pulse intervals of the green laser
        self.yellow_list=[]
        self.red_list=[]
        self.apd_list=[]
        self.micro_list=[]
        max_end_time=0
        self.max_iter_end=[]
        #IDEA: we could maybe add the dealy values like in the graph but for the simulation.
        #per one iteration
        #print(f"current:{self.iteration}")
        #print(f"iteration_all:{self.Iteration_All}")
        if self.iteration < self.max_iterations:
            #self.ui.current_iteration.setText(f"current iteration: ({self.iteration})")
            self.add_iteration_txt.emit(f"current iteration: ({self.iteration})")
            for i in range(len(self.Iteration_All)): #we iterate for all the channels
                Index=self.find_indices_first_terms(self.channel_labels,self.Iteration_All[i][0]) #we find the index of the channel on Iteration_ALl on the channel_labels list
                #now we can addres the label
                label=self.channel_labels[Index][1] #here we save the label 
                if len(self.Iteration_All[i])>1:#here we filter the channels that only have pulses on Iteration_All, and ad these lables to the 
                    All_labels.append(label)
                    #print(f"AllLabels:{All_labels}")
                    for j in range(len(self.Iteration_All[i])): #iterate through the amount of pulses per channel
                        if j>0:#after the channel index
                            #print(f"j:{j}")
                            if len(self.Iteration_All[i][j])==1: #in case there are no variatons to the pulse
                                # to grab the pulses that have no iter variations in the current iteration of the dinamic graph
                                #print("a pulse with NO variations")
                                unordered=[]
                                for z in range(len(self.Sequence_Pulses[i])): #we just do this to order the sequeunce pulses on this particular channel
                                    if z>0:
                                        unordered.append(self.Sequence_Pulses[i][z])   
                                ordered_sequence=sorted(unordered, key=lambda x: x[0])
                                #print(f"ordered_sequence:{label,ordered_sequence}")
                                if label.lower()=="green":
                                    self.green_list.append(ordered_sequence[j-1]) #we add the interval per channel in our list, #### we adedd the -1 because the ordered sequence doesnt have the channel so it would be out of range 
                                elif label.lower()=="yellow":
                                    self.yellow_list.append(ordered_sequence[j-1])
                                elif label.lower()=="red":
                                    self.red_list.append(ordered_sequence[j-1])
                                elif label.lower()=="apd":
                                    self.apd_list.append(ordered_sequence[j-1])
                                elif label.lower()=="microwave":
                                    self.micro_list.append(ordered_sequence[j-1])
                                        #print(f"Yellow_ordered 1 :{ yellow_ordered_int} ")
                                if max_end_time<ordered_sequence[j-1][1]: # if we find the max end time of between all the pulses to make alll the channels end in the same time in the graph 
                                    max_end_time=ordered_sequence[j-1][1] #### we adedd the -1 
                                    #print(f"max: {max_end_time}")
                                    #print(f"sequencepulses: {self.Sequence_Pulses[i][j]}")
                            else: # we enter a pulse which has a number of variations
                                #print("a pulse WITH variations")
                                for k in range(len(self.Iteration_All[i][j])): #we iterate through the variations
                                    if k>0: #because the k=0 is the pulse
                                        #print(f"k:{k}")
                                        #i_values=list(range(1, self.Iteration_All_PB[i][j][k][2][1]-self.Iteration_All_PB[i][j][k][2][0]+2)) # we create a list with all the iterations per iteration range in the current k index, example [56,57,58,59,60]
                                        i_values=list(range(self.Iteration_All_PB[i][j][k][2][0],self.Iteration_All_PB[i][j][k][2][1]+1))
                                        #print(f"ivalues: {i_values}") #the mistake is tha ivalues goes from 1 to infinity instead of between the index rangges
                                        if self.iteration in i_values :#we only do this operation if the iteration is inside the varying iteration values of the varying pulse and if the iteration is equal or bigger than the amount of interations there are, maybe its redundant idk
                                            #print(f"started_iteration:{self.iteration}")
                                            index_of_iteration= i_values.index(self.iteration) #+1 here we find the index of the iteration on the list i_values, ValueError: 0 is not in list
                                            #print(f"j:{j}")
                                            #print(f"k: {k}")
                                            #print(f"ivalues: {i_values}")
                                            #print(f"index_of_iteration:{index_of_iteration}")
                                            #print(f"Iteration_All:{self.Iteration_All}")
                                            #i_values_for_calculation = list(range(1,self.Iteration_All[i][j][k][1][1] - self.Iteration_All[i][j][k][1][0] +1)) #[1,2,3,4,5,6,7,8,9]
                                            #  add the new pulses to each corresponding list (channel_list)
                                            start_per_iter=self.Iteration_All[i][j][k][1] # this is giving me a diferent pulse start time
                                            end_per_iter=self.Iteration_All[i][j][k][3][index_of_iteration]+start_per_iter #index out of range!!!
                                            max_e_iter=self.Iteration_All[i][j][k][3][index_of_iteration] +start_per_iter
                                            #print(f"time:{start_per_iter,end_per_iter}")
                                            if max_end_time<max_e_iter: # if we find the max end time of between all the pulses to make alll the channels end in the same time in the graph 
                                                max_end_time=max_e_iter
                                            #print(f"max: {max_end_time}")
                                            #print(f"   ivalue[index]==iteration: {i_values[index_of_iteration]==self.iteration}")#######
                                        else:# the pulse with varying iter, now returns to its previous value
                                            unordered=[]
                                            for z in range(len(self.Sequence_Pulses[i])): #we just do this to order the sequeunce pulses on this particular channel
                                                if z>0:
                                                    unordered.append(self.Sequence_Pulses[i][z])   
                                            ordered_sequence=sorted(unordered, key=lambda x: x[0])
                                           #print(f"j-1:{j-1}")
                                            #print(f"ordered_sequence:{label,ordered_sequence}")
                                            start_per_iter=ordered_sequence[j-1][0]
                                            end_per_iter=ordered_sequence[j-1][1]
                                            max_end=end_per_iter 
                                            #print(f"max_end:{max_end}")
                                            if max_end_time<max_end: # if we find the max end time of between all the pulses to make alll the channels end in the same time in the graph 
                                                max_end_time=max_end
                                            pass
                                        if label.lower()=="green": 
                                            #if self.iteration in i_values  : # we check if the current iteration fall in this iteration range
                                            self.green_list.append([start_per_iter,end_per_iter]) #we add the interval per channel in our list
                                            #print(f"appended{[start_per_iter,end_per_iter]}")
                                            #print(f"iteration: {self.iteration}")
                                            #print(f"index_of_iteration{index_of_iteration}")
                                            #print(f"self.Iteration_All[i][j][k][3][index_of_iteration]: {self.Iteration_All[i][j][k][3][index_of_iteration]}")
                                            #print(f"self.Iteration_All[i][j][k][1]: {self.Iteration_All[i][j][k][1]}")       
                                            pass
                                        elif label.lower()=="yellow":
                                            self.yellow_list.append([start_per_iter,end_per_iter])
                                            pass
                                        elif label.lower()=="red":
                                            self.red_list.append([start_per_iter,end_per_iter])
                                            pass
                                        elif label.lower()=="apd":
                                            self.apd_list.append([start_per_iter,end_per_iter])
                                            pass
                                        elif label.lower()=="microwave":
                                            self.micro_list.append([start_per_iter,end_per_iter])
                                            pass  
 
            #print(f"green_list: {self.green_list}")
            green_ordered=sorted(self.green_list, key=lambda x: x[0]) #order the intervals in time from first to last 
            green_ordered_int = [[int(x) for x in sublist] for sublist in green_ordered] # to transfrom the float elements into integers
            #print(f"green_ordered_int: {green_ordered_int}")
            yellow_ordered=sorted(self.yellow_list, key=lambda x: x[0]) #order the intervals in time from first to last 
            yellow_ordered_int = [[int(x) for x in sublist] for sublist in yellow_ordered] # to transfrom the float elements into integers
            red_ordered=sorted(self.red_list, key=lambda x: x[0]) #order the intervals in time from first to last 
            #print(f"yellow_ordered_int: {yellow_ordered_int}")
            red_ordered_int = [[int(x) for x in sublist] for sublist in red_ordered] # to transfrom the float elements into integers
            #print(f"red_ordered_int: {red_ordered_int}")
            apd_ordered=sorted(self.apd_list, key=lambda x: x[0]) #order the intervals in time from first to last 
            apd_ordered_int = [[int(x) for x in sublist] for sublist in apd_ordered] # to transfrom the float elements into integers
            #print(f"apd_ordered_int: {apd_ordered_int}")
            micro_ordered=sorted(self.micro_list, key=lambda x: x[0]) #order the intervals in time from first to last 
            micro_ordered_int = [[int(x) for x in sublist] for sublist in micro_ordered] # to transfrom the float elements into integers
            for item in All_labels:
                if "green"==item.lower():
                    y_green=np.array([ 10 if any(start <= x < end for start, end in green_ordered_int) else 5 for x in np.arange(0, max_end_time, 1)]) 
                    x_green=np.linspace(0, max_end_time, len(y_green) + 1)# when using stepMode='center' in pyqtgraph, the length of the x array must be equal to the length of the y array plus one. This requirement ensures that each step has a starting and ending x-coordinate.
                    self.green_sequence = pg.PlotDataItem(x_green, y_green, stepMode='center',pen={'color': (44, 160, 44), 'width': 1.5}) # stepmpde allows us to graph with vertical lines
                    #self.ui.Simulation.addItem(self.green_sequence)
                    self.add_simulation_graph.emit(self.green_sequence)
                    #print(f"y_green:{}")
                    #print(f"ygreen={y_green}")
                    #print(f"ygreen={y_green}")
                elif "yellow"==item.lower():
                    y_yellow=np.array([ 20 if any(start <= x < end for start, end in yellow_ordered_int) else 15 for x in np.arange(0, max_end_time, 1)])
                    x_yellow=np.linspace(0, max_end_time, len(y_yellow) + 1)
                    self.yellow_sequence = pg.PlotDataItem(x_yellow, y_yellow, stepMode='center',pen={'color': (254, 198, 21), 'width': 1.5})
                    #self.ui.Simulation.addItem(self.yellow_sequence)
                    self.add_simulation_graph.emit(self.yellow_sequence)
                    #print("yellow ordered int 2")
                    #print(f"y_yellow: {y_yellow}")
                    #print(f"x_yellow {x_yellow}")
 
                elif "red"==item.lower():
                    y_red=np.array([ 30 if any(start <= x < end for start, end in red_ordered_int) else 25 for x in np.arange(0, max_end_time, 1)])
                    x_red=np.linspace(0, max_end_time, len(y_red) + 1)
                    self.red_sequence = pg.PlotDataItem(x_red, y_red,stepMode='center', pen={'color': (214, 39, 40), 'width': 1.5})
                    #self.ui.Simulation.addItem(self.red_sequence)
                    self.add_simulation_graph.emit(self.red_sequence)

                elif "apd"== item.lower():
                    y_apd=np.array([ 40 if any(start <= x < end for start, end in apd_ordered_int) else 35 for x in np.arange(0, max_end_time, 1)])
                    x_apd=np.linspace(0, max_end_time, len(y_apd) + 1)
                    self.apd_sequence = pg.PlotDataItem(x_apd, y_apd, stepMode='center', pen={'color': (250, 250, 250), 'width': 1.5})
                    #self.ui.Simulation.addItem(self.apd_sequence)
                    self.add_simulation_graph.emit(self.apd_sequence)

                elif "microwave" ==item.lower():
                    y_micro=np.array([ 50 if any(start <= x < end for start, end in micro_ordered_int)else 45 for x in np.arange(0, max_end_time, 1)])
                    x_micro=np.linspace(0, max_end_time, len(y_micro) + 1)
                    self.micro_sequence = pg.PlotDataItem(x_micro, y_micro,stepMode='center', pen={'color': (128, 0, 128), 'width': 1.5})
                    #self.ui.Simulation.addItem(self.micro_sequence)
                    self.add_simulation_graph.emit(self.micro_sequence)
        #print(f"iteration:{self.iteration}")
        if self.iteration<self.max_iterations:
            self.iteration= self.iteration +1  #we add one to the the iteration of the dinamic graph
        else: 
            self.timer.stop()
            self.iteration = 0
            #self.ui.Simulation.clear()
            self.clear_simulation_graph.emit()
            self.add_iteration_txt.emit(f"current iteration: ({self.iteration})")
            #self.ui.current_iteration.setText(f"current iteration: ({self.iteration})")
      




    duration_signal=Signal(str)
    def calculate_Loop_Duration(self,max_counter): #duration fo the pulse= sum of all the durations of each iteration
        # Initialize data
        counter=0
        max_counter=max_counter
        #max_counter=self.ui.Loop_Sequence.value()
        All_labels=[]
        self.green_list=[] #the pulse intervals of the green laser
        self.yellow_list=[]
        self.red_list=[]
        self.apd_list=[]
        self.micro_list=[]
        max_end_time=0
        self.duration=0
        for counter in range(max_counter):   
            max_end_time=0    
            if counter < max_counter:
                for i in range(len(self.Iteration_All)): #we iterate for all the channels
                    Index=self.find_indices_first_terms(self.channel_labels,self.Iteration_All[i][0]) #we find the index of the channel on Iteration_ALl on the channel_labels list
                    #now we can addres the label
                    label=self.channel_labels[Index][1] #here we save the label 
                    if len(self.Iteration_All[i])>1:#here we filter the channels that only have pulses on Iteration_All, and ad these lables to the 
                        All_labels.append(label)
                        #print(f"AllLabels:{All_labels}")
                        for j in range(len(self.Iteration_All[i])): #iterate through the amount of pulses per channel
                            if j>0:#after the channel index
                                #print(f"j:{j}")
                                if len(self.Iteration_All[i][j])==1: #in case there are no variatons to the pulse
                                    # to grab the pulses that have no iter variations in the current iteration of the dinamic graph
                                    #print("a pulse with NO variations")
                                    unordered=[]
                                    for z in range(len(self.Sequence_Pulses[i])): #we just do this to order the sequeunce pulses on this particular channel
                                        if z>0:
                                            unordered.append(self.Sequence_Pulses[i][z])   
                                    ordered_sequence=sorted(unordered, key=lambda x: x[0])
                                    #print(f"ordered_sequence:{label,ordered_sequence}")
                                
                                    if max_end_time<=ordered_sequence[j-1][1]: # if we find the max end time of between all the pulses to make alll the channels end in the same time in the graph 
                                        max_end_time=ordered_sequence[j-1][1] #### we adedd the -1 
                                        #print(f"max: {max_end_time}")
                                        #print(f"sequencepulses: {self.Sequence_Pulses[i][j]}")
                                else: # we enter a pulse which has a number of variations
                                    #print("a pulse WITH variations")
                                    for k in range(len(self.Iteration_All[i][j])): #we iterate through the variations
                                        if k>0:
                                            #print(f"k:{k}")
                                            i_values=list(range(1, self.Iteration_All[i][j][k][2][1]-self.Iteration_All[i][j][k][2][0]+2)) # we create a list with all the iterations per iteration range in the current k index, example [56,57,58,59,60]
                                            #print(f"ivalues: {i_values}")
                                            if (counter + 1) in i_values :#we only do this operation if the iteration is inside the varying iteration values of the varying pulse and if the iteration is equal or bigger than the amount of interations there are, maybe its redundant idk
                                                index_of_iteration= i_values.index(counter + 1) #+1 here we find the index of the iteration on the list i_values, ValueError: 0 is not in list
                                                #print(f"j:{j}")
                                                #print(f"k: {k}")
                                                #print(f"ivalues: {i_values}")
                                                #print(f"index_of_iteration:{index_of_iteration}")
                                                #print(f"Iteration_All:{self.Iteration_All}")
                                                #i_values_for_calculation = list(range(1,self.Iteration_All[i][j][k][1][1] - self.Iteration_All[i][j][k][1][0] +1)) #[1,2,3,4,5,6,7,8,9]
                                                #  add the new pulses to each corresponding list (channel_list)
                                                start_per_iter=self.Iteration_All[i][j][k][1] # this is giving me a diferent pulse start time
                                                end_per_iter=self.Iteration_All[i][j][k][3][index_of_iteration] + start_per_iter #index out of range!!!
                                                max_e_iter=self.Iteration_All[i][j][k][3][index_of_iteration] + start_per_iter
                                                if max_end_time<=max_e_iter: # if we find the max end time of between all the pulses to make alll the channels end in the same time in the graph 
                                                    max_end_time=max_e_iter
                                                #print(f"max: {max_end_time}")
                                                #print(f"   ivalue[index]==iteration: {i_values[index_of_iteration]==self.iteration}")#######
                                            else:# the pulse with varying iter, now returns to its previous value
                                                #print("not the variatons are over, retunr pt previous value")
                                                unordered=[]
                                                for z in range(len(self.Sequence_Pulses[i])): #we just do this to order the sequeunce pulses on this particular channel
                                                    if z>0:
                                                        unordered.append(self.Sequence_Pulses[i][z])   
                                                ordered_sequence=sorted(unordered, key=lambda x: x[0])
                                                #print(f"j-1:{j-1}")
                                                #print(f"ordered_sequence:{label,ordered_sequence}")
                                                start_per_iter=ordered_sequence[j-1][0]
                                                end_per_iter=ordered_sequence[j-1][1]
                                                max_end=end_per_iter 
                                                #print(f"max_end:{max_end}")
                                                if max_end_time<=max_end: # if we find the max end time of between all the pulses to make alll the channels end in the same time in the graph 
                                                    max_end_time=max_end
                                                pass
            self.duration=self.duration+max_end_time
        #print(f"Duration: ({self.duration})")
        duration_str=f"Duration:{self.duration}"
        self.duration_signal.emit(duration_str)
        #self.ui.Duration_Loop.setText(f"Duration:{self.duration}")
        pass




    def stop_simulation(self):
        if self.iteration>0:
            self.timer.stop()
            self.iteration = 0
            #self.ui.Simulation.clear()
            self.clear_simulation_graph.emit()
        pass







    def order_intended_pulses(self): #order pulse blaster sequence in time 
        if all(len(self.Sequence_Pulses[i])==1 for i in range(len(self.Sequence_Pulses))):
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText("No pulses added")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        else:
            flattened_intervals = []
            for channel_data in self.Sequence_Pulses:
                channel = channel_data[0]
                intervals = channel_data[1:]
                for interval in intervals:
                    flattened_intervals.append((channel, interval))
            #print("flattened_intervals")
            #print(flattened_intervals)

            # Sort intervals by start time, then by end time
            flattened_intervals.sort(key=lambda x: (x[1][0], x[1][1]))
            #print("flattened_intervals sorted")
            #print(flattened_intervals)

            # Merge intervals with the same start and end times
            merged_intervals = []
            for channel, interval in flattened_intervals:
                if merged_intervals and merged_intervals[-1][1] == interval:
                    # Merge channels with the same interval
                    merged_intervals[-1][0] = tuple(sorted(merged_intervals[-1][0] + (channel,)))
                else:
                    # Add a new interval
                    merged_intervals.append([(channel,), interval])
            #print("merged intervals")
            #print(merged_intervals)

            # Simplify single-channel tuples to integers
            for i in range(len(merged_intervals)):
                if len(merged_intervals[i][0]) == 1:
                    merged_intervals[i][0] = merged_intervals[i][0][0]

            #print("updated merged intervals")
            #print(merged_intervals)

            # Split intervals with overlapping channels
            self.final_result = []
            for i in range(len(merged_intervals)):
                if i > 0 and merged_intervals[i][1][0] < merged_intervals[i-1][1][1]:
                    overlap_start = merged_intervals[i][1][0]
                    overlap_end = min(merged_intervals[i][1][1], merged_intervals[i-1][1][1])
                    merged_intervals[i-1][1][1] = overlap_start
                    if isinstance(merged_intervals[i-1][0], int):
                        merged_intervals[i-1][0] = (merged_intervals[i-1][0],)
                    if isinstance(merged_intervals[i][0], int):
                        merged_intervals[i][0] = (merged_intervals[i][0],)
                    self.final_result.append([tuple(sorted(set(merged_intervals[i-1][0]).union(set(merged_intervals[i][0])))), [overlap_start, overlap_end]])
                    if overlap_end < merged_intervals[i][1][1]:
                        merged_intervals[i][1][0] = overlap_end
                        self.final_result.append(merged_intervals[i])
                else:
                    self.final_result.append(merged_intervals[i])

            #print("Final Result")
            #print(self.final_result)

        # Remove intervals with the same start and end time
        self.final_result = [interval for interval in self.final_result if interval[1][0] != interval[1][1]]

        # Simplify single-channel tuples to integers in the final result
        for i in range(len(self.final_result)):
            if isinstance(self.final_result[i][0], tuple) and len(self.final_result[i][0]) == 1:
                self.final_result[i][0] = self.final_result[i][0][0]
        # Output the ordered intervals
        #print("Final Result")
        #print(self.final_result)
        return self.final_result
    
    def order_pb_pulses(self): #order pulse blaster sequence in time 
        if all(len(self.pb_pulses[i])==1 for i in range(len(self.pb_pulses))):
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText("No pulses added")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        else:
            flattened_intervals = []
            for channel_data in self.pb_pulses:
                channel = channel_data[0]
                intervals = channel_data[1:]
                for interval in intervals:
                    flattened_intervals.append((channel, interval))
            #print("flattened_intervals")
            #print(flattened_intervals)

            # Sort intervals by start time, then by end time
            flattened_intervals.sort(key=lambda x: (x[1][0], x[1][1]))
            #print("flattened_intervals sorted")
            #print(flattened_intervals)

            # Merge intervals with the same start and end times
            merged_intervals = []
            for channel, interval in flattened_intervals:
                if merged_intervals and merged_intervals[-1][1] == interval:
                    # Merge channels with the same interval
                    merged_intervals[-1][0] = tuple(sorted(merged_intervals[-1][0] + (channel,)))
                else:
                    # Add a new interval
                    merged_intervals.append([(channel,), interval])
            #print("merged intervals")
            #print(merged_intervals)

            # Simplify single-channel tuples to integers
            for i in range(len(merged_intervals)):
                if len(merged_intervals[i][0]) == 1:
                    merged_intervals[i][0] = merged_intervals[i][0][0]

            #print("updated merged intervals")
            #print(merged_intervals)

            # Split intervals with overlapping channels
            self.final_result = []
            for i in range(len(merged_intervals)):
                if i > 0 and merged_intervals[i][1][0] < merged_intervals[i-1][1][1]:
                    overlap_start = merged_intervals[i][1][0]
                    overlap_end = min(merged_intervals[i][1][1], merged_intervals[i-1][1][1])
                    merged_intervals[i-1][1][1] = overlap_start
                    if isinstance(merged_intervals[i-1][0], int):
                        merged_intervals[i-1][0] = (merged_intervals[i-1][0],)
                    if isinstance(merged_intervals[i][0], int):
                        merged_intervals[i][0] = (merged_intervals[i][0],)
                    self.final_result.append([tuple(sorted(set(merged_intervals[i-1][0]).union(set(merged_intervals[i][0])))), [overlap_start, overlap_end]])
                    if overlap_end < merged_intervals[i][1][1]:
                        merged_intervals[i][1][0] = overlap_end
                        self.final_result.append(merged_intervals[i])
                else:
                    self.final_result.append(merged_intervals[i])

            #print("Final Result")
            #print(self.final_result)

        # Remove intervals with the same start and end time
        self.final_result = [interval for interval in self.final_result if interval[1][0] != interval[1][1]]

        # Simplify single-channel tuples to integers in the final result
        for i in range(len(self.final_result)):
            if isinstance(self.final_result[i][0], tuple) and len(self.final_result[i][0]) == 1:
                self.final_result[i][0] = self.final_result[i][0][0]
        # Output the ordered intervals
        #print("Final Result")
        #print(self.final_result)
        return self.final_result
    
    def order_general_pulses(self,LIST): #order pulse blaster sequence in time 
        if all(len(LIST[i])==1 for i in range(len(LIST))):
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Error!")
            dlg.setText("No pulses added")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec_()
        else:
            flattened_intervals = []
            for channel_data in LIST:
                channel = channel_data[0]
                intervals = channel_data[1:]
                for interval in intervals:
                    flattened_intervals.append((channel, interval))
            #print("flattened_intervals")
            #print(flattened_intervals)

            # Sort intervals by start time, then by end time
            flattened_intervals.sort(key=lambda x: (x[1][0], x[1][1]))
            #print("flattened_intervals sorted")
            #print(flattened_intervals)

            # Merge intervals with the same start and end times
            merged_intervals = []
            for channel, interval in flattened_intervals:
                if merged_intervals and merged_intervals[-1][1] == interval:
                    # Merge channels with the same interval
                    merged_intervals[-1][0] = tuple(sorted(merged_intervals[-1][0] + (channel,)))
                else:
                    # Add a new interval
                    merged_intervals.append([(channel,), interval])
            #print("merged intervals")
            #print(merged_intervals)

            # Simplify single-channel tuples to integers
            for i in range(len(merged_intervals)):
                if len(merged_intervals[i][0]) == 1:
                    merged_intervals[i][0] = merged_intervals[i][0][0]

            #print("updated merged intervals")
            #print(merged_intervals)

            # Split intervals with overlapping channels
            self.final_result = []
            for i in range(len(merged_intervals)):
                if i > 0 and merged_intervals[i][1][0] < merged_intervals[i-1][1][1]:
                    overlap_start = merged_intervals[i][1][0]
                    overlap_end = min(merged_intervals[i][1][1], merged_intervals[i-1][1][1])
                    merged_intervals[i-1][1][1] = overlap_start
                    if isinstance(merged_intervals[i-1][0], int):
                        merged_intervals[i-1][0] = (merged_intervals[i-1][0],)
                    if isinstance(merged_intervals[i][0], int):
                        merged_intervals[i][0] = (merged_intervals[i][0],)
                    self.final_result.append([tuple(sorted(set(merged_intervals[i-1][0]).union(set(merged_intervals[i][0])))), [overlap_start, overlap_end]])
                    if overlap_end < merged_intervals[i][1][1]:
                        merged_intervals[i][1][0] = overlap_end
                        self.final_result.append(merged_intervals[i])
                else:
                    self.final_result.append(merged_intervals[i])

            #print("Final Result")
            #print(self.final_result)

        # Remove intervals with the same start and end time
        self.final_result = [interval for interval in self.final_result if interval[1][0] != interval[1][1]]

        # Simplify single-channel tuples to integers in the final result
        for i in range(len(self.final_result)):
            if isinstance(self.final_result[i][0], tuple) and len(self.final_result[i][0]) == 1:
                self.final_result[i][0] = self.final_result[i][0][0]
        # Output the ordered intervals
        #print("Final Result")
        #print(self.final_result)
        return self.final_result
    





    
    def order_specific_Channels_Pulses(self,List): #List must be like [channel,[start,end],[start,end]]
        unordered=[]
        for i in range(len(List)):
            if i>0:
                unordered.append(List[i]) #we leave only the intervals and not the channel
        ordered=sorted(unordered, key=lambda x: x[0])#sorts a list of lists (or tuples) named unordered based on the first element of each sublist (or tuple).
        return ordered

    def pulses_ordered_by_time_channels_pb(self): #here we prepare the variable self.All_Lists=[[channel, ordered pulses], ]
        channels_with_pulses=[]
        self.All_List_PB=[]
        ordered=self.order_pb_pulses()
        #print(f"ordered_pulses_pb: {ordered}")
        #now we need to get a list with all the channels that have pulses
        for i in range(len(self.pb_pulses)):
            channels_with_pulses.append(self.pb_pulses[i][0])
        for i in range(len(channels_with_pulses)):
            filtered_list=[[channels_with_pulses[i], item[1]] for item in ordered if (isinstance(item[0], int) and item[0] == channels_with_pulses[i]) or (isinstance(item[0], tuple) and channels_with_pulses[i] in item[0])] 
            #print(f"fultered_list: {filtered_list}")
            for j in range(len(filtered_list)):
                #print(f"j:{j}") 
                if j==0:
                    self.All_List_PB.append([channels_with_pulses[i]])
                    index_channel=len(self.All_List_PB)-1
                    #print(f"index_channel: {index_channel}")
                    self.All_List_PB[index_channel].append(filtered_list[j][1])
                else:
                    self.All_List_PB[index_channel].append(filtered_list[j][1])
        #print("after calling the function")
        #print(f"All_list_pb_inside: {self.All_List_PB}")
        return self.All_List_PB
    def pulses_ordered_by_time_channels(self): #here we prepare the variable self.All_Lists=[[channel, ordered pulses], ]
        channels_with_pulses=[]
        self.All_List=[]
        ordered_pb=self.order_intended_pulses()
        #print(f"ordered_pulses_intended: {ordered_pb}")
        #now we need to get a list with all the channels that have pulses
        for i in range(len(self.pb_pulses)):
            channels_with_pulses.append(self.Sequence_Pulses[i][0])
        for i in range(len(channels_with_pulses)):
            filtered_list=[[channels_with_pulses[i], item[1]] for item in ordered_pb if (isinstance(item[0], int) and item[0] == channels_with_pulses[i]) or (isinstance(item[0], tuple) and channels_with_pulses[i] in item[0])] 
            for j in range(len(filtered_list)):
                #print(f"j:{j}") 
                if j==0:
                    self.All_List.append([channels_with_pulses[i]])
                    index_channel=len(self.All_List)-1 
                    #print(f"index_channel: {index_channel}")
                    self.All_List[index_channel].append(filtered_list[j][1])
                else:
                    self.All_List[index_channel].append(filtered_list[j][1])
        #print("after calling the fucntion")
        #print(f"All_list: {self.All_List}")

        return self.All_List
    

    def clear_list(self): #should basically restart everyhting
        self.channel_labels=[] #[[channel, label],[channel, label]]
        self.added_channels = []
        self.added_flags=[]
        self.pb_pulses=[] # here we keep all the pulses added from all the channels,adjusted for the delays, this is for the pulse blaster
        self.Sequence_Pulses=[]
        self.green_list=[]
        self.yellow_list=[]
        self.red_list=[]
        self.apd_list=[]
        self.micro_list=[]
        self.final_result=[]
        self.Channel_Pulse_iter=[]
        self.All_List=[] # [ [channe,[,],[,]], [channle,[,],[,]] ] ordered pulses
        self.All_List_PB=[]
        self.Max_end_type=[] #[ [channel,[pulse,[type],[max_end]]], [channel,.....]]
        self.iteration_list_saving=[]
        self.Iteration_All=[] 
        self.Start_Results=[]
        self.Global_end_time=0
        self.duration=0
        self.Delays_channel=[]
        self.green_list_pb=[]
        self.yellow_list_pb=[]
        self.apd_list_pb=[]
        self.red_list_pb=[]
        self.micro_list_pb=[]
        self.Iteration_All_PB=[]
        # here we start with a basic plot, which gets updated, if we either add channels, or we add pulses in thoses channels

    def contains_sublists(self,lst):
        for item in lst:
            if isinstance(item, list):  # Check if the item is a list
                if any(isinstance(subitem, list) for subitem in item):  # Check if any subitem is a list
                    return True
                if self.contains_sublists(item):  # Recursively check the sublist
                    return True
        return False
            
    


#Now we proceed to added the pulses groupbox fromt the gui
#but first we create a fucntion that allows us to find indexes of a list of lists, this will help us later
    def find_indices_first_terms(self,nested_list, target): # i: A variable that will hold the index of the current sublist.enumerate(nested_list): A built-in function that allows you to iterate over nested_list while keeping track of both the index (i) and the element (sublist). sublist: A variable that will hold the current sublist from nested_list. for: Starts a loop to iterate over nested_list.
        for i, sublist in enumerate(nested_list): # sublist: A variable that will hold the current sublist from nested_list. The enumerate function in Python adds a counter to an iterable (like a list) and returns it as an enumerate object. This allows you to loop over the iterable and have access to both the index and the value of each element.
        # Check if the sublist is a list and has at least one element
            if isinstance(sublist, list) and len(sublist) > 0:#isinstance(sublist, list): Checks if sublist is indeed a list.
                if sublist[0] == target:  # Compare with the first element of the sublist
                    return i  # Return the index at the top level
        return None  # Return None if no match is found
    
#find an element in a list of lists
    def find_index(self,list_of_lists, target):
        for i, sublist in enumerate(list_of_lists):
            if target in sublist:
                return (i, sublist.index(target))
        return None

    def Run_experiment(self,value_loop,channel_count): 

        # Create the sequence
        #counter=0
        max_iterations=value_loop
        #first we need to add the pulses to of the current iteration to a list
        self.channels_conversion(channel_count) #here we get the values in decimal form of the repective channels
        # we can acces them in the list self.decimal_channel
        #instead of adding the tao time, we simply get the previous pulseen end time and the next pulse start time and we substract them
        #print("Experiment runned")
        #print(f"max_iter:{max_iterations}")
        #HALF THE PART OF THIS FUNCITON IS TO CREATE A LIST CALLED:
        self.PULSE_BLASTER=[]
        #BUT FIRST WE NEED TO START BY CREATING ANOTHER LIST: All_pulses which is[ [channel,[start,end],[start,end]], [channel,[start,end]] were per each channel the pulse sequence is ordered
        for x in range(1,max_iterations+2): 
            #print(f"x:{x}")
            #All_channels=[]
            sequence_per_iter=[]   
            #print(f"iteration_all_pb: {self.Iteration_All_PB}")         
            for i in range(len(self.Iteration_All_PB)): #we iterate for all the channels
                Index=self.find_indices_first_terms(self.channel_labels,self.Iteration_All_PB[i][0]) #we find the index of the channel on Iteration_ALl_PB on the channel_labels list
                #now we can addres the label
                channel=self.channel_labels[Index][0] #here we save the label 
                All_pulses=[]
                if len(self.Iteration_All_PB[i])>1:#here we filter the channels that only have pulses on Iteration_All, must be bigger than 1 because 1 is the channel 
                    #All_channels.append([channel])
                    #print(f"AllLabels:{All_labels}")
                    for j in range(len(self.Iteration_All_PB[i])): #iterate through the amount of pulses per this channel
                        if j>0:#after the channel index
                            #print(f"j:{j}")
                            if len(self.Iteration_All_PB[i][j])==1: #in case there are no variatons to the pulse
                                # to grab the pulses that have no iter variations in the current iteration of the dinamic graph
                                #print(f"a pulse with NO variations{self.Iteration_All_PB[i][j]}")
                                unordered=[]
                                for z in range(len(self.pb_pulses[i])): #we just do this to order the sequeunce pulses on this particular channel, pb_pulses should be sinchronized with Iteration_All
                                    if z>0:
                                        unordered.append(self.pb_pulses[i][z])   
                                ordered_sequence=sorted(unordered, key=lambda x: x[0])
                                #print(f"ordered-s:{ordered_sequence}")
                                start_per_iter=ordered_sequence[j-1][0]
                                end_per_iter=ordered_sequence[j-1][1]
                                All_pulses.append([start_per_iter,end_per_iter])
                            else: # we enter a pulse which has  variations
                                #print("a pulse WITH variations")
                                for k in range(len(self.Iteration_All_PB[i][j])): #we iterate through the variations
                                    if k>0: #because the k=0 is the pulse
                                        #print(f"k:{k}")
                                        i_values=list(range(1, self.Iteration_All_PB[i][j][k][2][1]-self.Iteration_All_PB[i][j][k][2][0]+2)) # we create a list with all the iterations per iteration range in the current k index, example [56,57,58,59,60] if the range is [56,60]
                                        #print(f"ivalues: {i_values}")
                                        if x in i_values :#we only do this operation if the iteration is inside the varying iteration values of the varying pulse and if the iteration is equal or bigger than the amount of interations there are, maybe its redundant idk
                                            index_of_iteration= i_values.index(x) #+1 here we find the index of the iteration on the list i_values
                                            #print(f"j:{j}")
                                            #print(f"k: {k}")
                                            #print(f"ivalues: {i_values}")
                                            #print(f"index_of_iteration:{index_of_iteration}")
                                            #print(f"Iteration_All:{self.Iteration_All}")
                                            #i_values_for_calculation = list(range(1,self.Iteration_All[i][j][k][1][1] - self.Iteration_All[i][j][k][1][0] +1)) #[1,2,3,4,5,6,7,8,9]
                                            #  add the new pulses to each corresponding list (channel_list)
                                            start_per_iter=self.Iteration_All_PB[i][j][k][1] 
                                            end_per_iter=self.Iteration_All_PB[i][j][k][3][index_of_iteration]+start_per_iter 
                                            All_pulses.append([start_per_iter,end_per_iter])
                                        else:# the pulse with varying iter, now returns to its previous value
                                            unordered=[]
                                            for z in range(len(self.pb_pulses[i])): #we just do this to order the sequeunce pulses on this particular channel
                                                if z>0:
                                                    unordered.append(self.pb_pulses[i][z])   
                                            ordered_sequence=sorted(unordered, key=lambda x: x[0])
                                           #print(f"j-1:{j-1}")
                                            #print(f"ordered_sequence:{ordered_sequence}")
                                            start_per_iter=ordered_sequence[j-1][0]
                                            end_per_iter=ordered_sequence[j-1][1]
                                            All_pulses.append([start_per_iter,end_per_iter])
                                            pass
                All_pulses=sorted(All_pulses, key=lambda x: x[0]) # by now we have Allpulses= [ [start,end],[],[]..] we must order it
                #print(f"All_pulses:{All_pulses}")
                All_pulses.insert(0,channel)# we put a channel infron of the ordered pulse sequence in this list
                #print(f"All_pulses:{All_pulses}")
                sequence_per_iter.append(All_pulses) # sequence_per_iter gets this shape [ [channel,[start,end],[start,end]] , [channe...]]] the pulses are ordered inside each channel however the channels between themselves are not ordered
                sequence_per_iter= self.order_general_pulses(sequence_per_iter) #this functions orders the list, leaving it as [ [channel/s,[start,end]], [chann...]...]
                #print(f"sequence per iter:{sequence_per_iter}") 
            self.PULSE_BLASTER.append([x-1 ,sequence_per_iter]) # this list gets this shape[ [iteration,[ [channel/s,[start,end]], [chann...]...]], [iteration,.......] ]
            print(f"Pulse_Blaster:{self.PULSE_BLASTER}")
        ######we could make this another function
        dt=0 # dark time, no pulses ON, its decimal value must be cero
        ######we could turn this into a function
        
        #print(f"channel/s and its decimal value: {channel,decimal_value}")
        #print(f"star and end time: {self.PULSE_BLASTER[counter][1][0][1]}")
        self.PB_WIDTH=[]
        #spinapi.pb_start_programming(spinapi.PULSE_PROGRAM) # the pulse program will be programmed using pb_inst instructions, it also it tells the board to start programming  the pulse sequence
        #if start_time>0: #if the first pulse starts after time cero, the first instruction must be a delay
            #print(f"there is a delay at the start of {start_time}")
            #start=spinapi.pb_inst_pbonly(dt,Inst.LOOP,int(self.ui.Loop_Sequence.value()),(start_time)*spinapi.us)
            #print(f"spinapi.pb_inst_pbonly({dt},Inst.LOOP,int({self.ui.Loop_Sequence.value()}),({start_time})*spinapi.us)")
            #spinapi.pb_inst_pbonly(decimal_value,Inst.CONTINUE,0,(end_time-start_time)*spinapi.us)
            #print(f"spinapi.pb_inst_pbonly({decimal_value},Inst.CONTINUE,0,({end_time-start_time})*spinapi.us)")
            
        #else:   
            #print(f"there is a pulse first, not a delay")
            #start=spinapi.pb_inst_pbonly(decimal_value,Inst.LOOP,int(self.ui.Loop_Sequence.value()),(self.PULSE_BLASTER[1][0][1][1]-self.PULSE_BLASTER[counter][1][0][1][0])*spinapi.us)
            #print(f"spinapi.pb_inst_pbonly({decimal_value},Inst.CONTINUE,0,({end_time-start_time})*spinapi.us)")
        #if len(self.PULSE_BLASTER[counter][1])>1: # to see if there are more pulses (not including the first one) on this iteration
        print(f"len(PULSE_BLASTER:{len(self.PULSE_BLASTER)})") #should be one less
        for counter in range(len(self.PULSE_BLASTER)):
            print(f"counter:{counter}")
            print(f"self.PULSE_BLASTER[{counter}][1]--> pulses per iteration:{self.PULSE_BLASTER[counter][1]}")
            for i in range(len(self.PULSE_BLASTER[counter][1])): # we iterate for the amount of pulses per iteration (counter)
                start_time=self.PULSE_BLASTER[counter][1][i][1][0]
                print(f"start_time:{start_time}")
                end_time=self.PULSE_BLASTER[counter][1][i][1][1]
                channel=self.PULSE_BLASTER[counter][1][i][0]
                print(f"end_time:{end_time}")
                print(f"i:{i}")
                if i==0:
                    if start_time>0: #if the first pulse starts after time cero, the first instruction must be a delay
                        print(f"there is a delay at the start of {start_time}")
                        self.PB_WIDTH.append([dt,start_time]) # here we add the dark time to the isntruction list
                        decimal_value=self.finding_decimal_channel(channel) # we must transform the channel value to decimal form
                        self.PB_WIDTH.append([decimal_value,end_time-start_time]) # here we add the next instruction to the list
                        #print(f"PB_WIDTH:{self.PB_WIDTH}")
                    else:
                        decimal_value=self.finding_decimal_channel(channel)
                        self.PB_WIDTH.append([decimal_value,end_time-start_time])
                        #print(f"PB_WIDTH:{self.PB_WIDTH}")
                            
                else:
                    previous_end_time=self.PULSE_BLASTER[counter][1][i-1][1][1]
                    #print(f"PB_WIDTH:{self.PB_WIDTH}")
                    print(f"previous_end:{previous_end_time}")
                    if previous_end_time!=start_time:# if the condition is met, it means there is darktime between the two pulses, before the next pulse
                        self.PB_WIDTH.append([dt,start_time-previous_end_time])
                    decimal_value=self.finding_decimal_channel(channel)
                    print(f"decimal_value:{decimal_value}")
                    self.PB_WIDTH.append([decimal_value,end_time-start_time])
        print(f"PB_WIDTH:{self.PB_WIDTH}")
        self.Send_Pulse_Blaster() #now we continue printing zending the instrucitons to the pulse blaster

    def Send_Pulse_Blaster(self):
        #spinapi.pb_init()
        #spinapi.pb_start()
        #spinapi.pb_start_programming(spinapi.PULSE_PROGRAM)
        #start=spinapi.pb_inst_pbonly(int(self.PB_WIDTH[0][0]),Inst.LOOP,1,(self.PB_WIDTH[0][1])*spinapi.us)
        print(f"spinapi.pb_inst_pbonly({self.PB_WIDTH[0][0]},Inst.LOOP,{1},({self.PB_WIDTH[0][1]})*spinapi.us)") # we only do one iteration because PB_WIDTH has all of the iterations
        for i in range(1,len(self.PB_WIDTH)):# we start from one because we already did the 0 index
            if i!=len(self.PB_WIDTH) -1:
                print(f"spinapi.pb_inst_pbonly({self.PB_WIDTH[i][0]},Inst.CONTINUE,0,({self.PB_WIDTH[i][1]})*spinapi.us)")
                #spinapi.pb_inst_pbonly(int(self.PB_WIDTH[i][0]),Inst.CONTINUE,0,(self.PB_WIDTH[i][1])*spinapi.us)
            else:
                print(f"spinapi.pb_inst_pbonly({self.PB_WIDTH[i][0]},Inst.CONTINUE,0,({self.PB_WIDTH[i][1]})*spinapi.us)")
                #spinapi.pb_inst_pbonly(int(self.PB_WIDTH[i][0]),Inst.CONTINUE,0,(self.PB_WIDTH[i][1])*spinapi.us)
                print(f"spinapi.pb_inst_pbonly({self.PB_WIDTH[i][0]},Inst.END_LOOP,start,{self.PB_WIDTH[i][1]}")
                #spinapi.pb_inst_pbonly(int(self.PB_WIDTH[i][0]),Inst.END_LOOP,start,self.PB_WIDTH[i][1])
        #spinapi.pb_inst_pbonly(int(0),Inst.STOP,0,0.01*spinapi.us) # This instruction stops the pulse sequence. The duration is set to a very small value to ensure the stop instruction is executed almost immediately.
        print(f"spinapi.pb_inst_pbonly(int(0),Inst.STOP,0,0.01*spinapi.us)")
        #spinapi.pb_stop_programming()  # This function call signals the end of programming the pulse sequence. It tells the SpinAPI library that the sequence definition is complete and the pulse program can be finalized
        print(f"spinapi.pb_stop_programming()")

        pass






    def finding_decimal_channel(self,channel):
        decimal_value=0
        if isinstance(channel, tuple) or isinstance(channel,list): # we check if more than one channel is activated, and get the decimal value
            #print(f"decimal_channel:{self.decimal_channel}")
            for j in range(len(channel)):
                index_decimal=self.find_indices_first_terms(self.decimal_channel,channel[j])
                decimal=self.decimal_channel[index_decimal][1]
                #print(f"decimal_found:{self.decimal_channel[index_decimal][1]}")
                decimal_value=decimal+decimal_value
        else: #it means there is only one channel
            index_decimal=self.find_indices_first_terms(self.decimal_channel,channel)
            decimal=self.decimal_channel[index_decimal][1]
            decimal_value=decimal+decimal_value
        return decimal_value        

    def channels_conversion(self,channel_count):
        #we must first create a binary chain with as many ceros as there are channels
        binary=[]
        self.decimal_channel=[]
        for i in range(channel_count):
            binary.append(0)
        #print(f"binary:{binary}")
        #create the binary number as a string per each channel which is in self.added_channels
        for i in range(len(binary)):
            binary_channel=binary.copy()# must do this because otherwise the list will be linked
            if i in self.added_channels:
                #print(f"binary_channel:{binary_channel}")
                binary_channel[-(i+1)]=1#[-(i+1)]
                binary_str=''.join(map(str, binary_channel))
                #print(f"binary_str:{binary_str}")
                decimal=self.binary_to_integer(binary_str)
                #print(f"decimal:{decimal}")
                self.decimal_channel.append([i,decimal])
        #print(f"decimal_channel:{self.decimal_channel}")

    def binary_to_integer(self,binary_str):
        """
        Convert a binary string to an integer.
    
        Args:
        binary_str (str): A string representing a binary number (e.g., '1010').
    
        Returns:
        int: The integer representation of the binary string.
        """
        try:
            # Convert binary string to integer using base 2
            integer_value = int(binary_str, 2)
            return integer_value
        except ValueError:
            # Handle the case where the input is not a valid binary string
            print(f"Error: '{binary_str}' is not a valid binary string.")
            return None