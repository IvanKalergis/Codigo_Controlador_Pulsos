#Clase para añadir canales a la base de datos
from Pulse_class import Pulse
from PySide2.QtCore import QObject , Signal

#We chose to leave the channel class to leave the atributtes a channel needs to have in order to be created, and also the requirments it need to serve. 
# Otherwise if it violates the requirments it will let the user know, and it will not be created.
class Channel:


    def __init__(self, tag, label, delay):
        #for each channel
        self.tag = tag
        self.label = label
        self.delay = delay

        # For the sequence of pulses, here we could leave pb_pulses or sequence_pulses
        self.pulse_list = []

    def add_pulse(self, pulse_delay, pulse_width, pulse_channel_tag):

        pulse = Pulse(pulse_delay, pulse_width, pulse_channel_tag)
        status = self.check_pulse_compability(pulse)
        if status is True:
            self.pulse_list.append(pulse)


    
    def check_pulse_compability(self, pulse):

        pass

    def clear(self):
        self.pulse_list = []

    def get_display_list(self):
        """
        Returns a list with the pulse information for display.

        # Probably need some adjustments
        """
        display_list = []
        """for pulse in self.pulse_list:
            display_list.append((pulse.pulse_delay, pulse.pulse_width, pulse.pulse_channel_tag))"""
        return display_list
    error_adding_pulse=Signal(str)
    def Added_Pulses(self,start_time,width):
        
        #the value of the channel   
        #we need to adjust the intervals to account for the delays 
        #including the delays
        delay_on=self.delay[0]
        delay_off=self.delay[1]
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
                #now we check if its possible account for the delays in the specific channel (checking if there are any other pulses in the same channel, that overlap with these intervals)
                #allows me to not get an error: List index out of range in the first iteration
            Index = self.find_indices_first_terms(self.pb_pulses, int(channel_tag) ) # we get the index of the combobox which is the value of the channel, we find the index of this value on pb_pulses
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
                    self.error_adding_pulse.emit(f"Overlapping pulses in channel {channel_}")
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
    return [self.pb_pulses] # this is the sequence that will be used for the pulse blaster"""
