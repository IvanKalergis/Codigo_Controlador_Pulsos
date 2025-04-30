#Clase para añadir canales a la base de datos
from Pulse_class import Pulse
from PySide2.QtCore import QObject , Signal


class Sequence: #A sequence per iteration ( 1 frame)
    def __init__(self,iteration,tag):
        self.tag=tag #the channel tag (ex: PB0, PB1, etc)
        self.iteration=iteration #iteration of the sequence, meaning ex: the sequence appears in the 50th iteration of the experiment
        self.pb_pulses=[] # this is the list of the instances of pulses of this particular sequence that will be sent to the pulse blaster (accounting for delays)
        self.pulses=[]  #this is the list of the instances of pulses shown in the simulation.
        #elf.Channel_Pulse_iter=[] # this is the list of the pulses in the channel, it will be used to check for overlapping, WE MIGHT NOT NEED THIS
        self.max_end_time_pb=0 # this is the end time of the sequence, it will be used to check if the pulse blaster is ready to send the next sequence
        self.max_end_time=0
    
    error_adding_pulse=Signal(str)
    def add_pulse(self, start_time,width,delay_on,delay_off): 
        end_tail=start_time+width
        start_tail=start_time
        pulse=Pulse(start_tail,end_tail) #without delays
        end_tail=start_time+width-delay_off
        start_tail=start_time-delay_on
        pulse_pb = Pulse(start_tail,end_tail) #with delays
        status = self.check_pulse_compability(pulse_pb,delay_off,width) #check if the pulse doensnt overlap
        if status is True:
            self.pb_pulses.append(pulse_pb)
            self.pulses.append(pulse)
        

    
    def check_pulse_compability(self,pulse_pb,delay_off,width):
        """
        Here we must aim o see if the corresponding pulse overlaps with any of the the pb_pulses 
        """
        #the value of the channel   
        #we need to adjust the intervals to account for the delays 
        #including the delays
        start_tail=pulse_pb.start_tail
        end_tail=pulse_pb.end_tail
        Adjusted_Interval=[start_tail,end_tail] #specifically for the Pulse_Blaster, these are the intervals that account for the delays to maintain the intended timeframes
        
        pulse_collapse=False
        if delay_off>=width:
            pulse_collapse=True
            self.error_adding_pulse.emit(f"Pulse delay_off={delay_off}>{width}=width")
        overlap_fixed_pulses=False #we define this variable to let the system know when there is an overlap with the fixed pulses
        if Adjusted_Interval[0]>=0 and pulse_collapse==False: #if the adjustes_interval starts after or on 0=t, to avoid negative time 
                #now we check if its possible account for the delays in the specific channel (checking if there are any other pulses in the same channel, that overlap with these intervals)
                #allows me to not get an error: List index out of range in the first iteration
            
            if len(self.pb_pulses) > 0 : #if there are other puslse on the same channel we need to check for overlapping, and we also check if the list on the index has a sublist
                for j in range(len(self.pb_pulses)): #we iterate over the pb_pulses in the respective channel, to check for overlapping
                    if j>0:
                        Partially_Left=(self.pb_pulses[j].start_tail<=end_tail and self.pb_pulses[0]>=start_tail) # if the the new pulse finishes after the start of the previous pulse and starts before the start of the previous pulse
                        Partially_Right=(self.pb_pulses[j].end_tail<=end_tail and self.pb_pulses[j].end_tail>=start_tail) # if the new pulse finishes after the end of the previous pulse and starts before the end of the previous pulse
                        Completely_Inside=(self.pb_pulses[j].start_tail<=start_tail and self.pb_pulses[j].end_tail>=end_tail) #if the new pulse starts after the start of the previous pulse and finishes before the end of the previous pulse
                        Completely_Ontop=(self.pb_pulses[j].start_tail>=start_tail and self.pb_pulses[j].end_tail<=end_tail)
                        
                        if Partially_Left==True or Partially_Right==True or Completely_Inside==True or Completely_Ontop==True: #if the pulse is partially, or completely inside the interval the overlap varible becomes true
                            overlap_fixed_pulses=True
                            break #we stop the loop since we already found an overlap
                if overlap_fixed_pulses==True: 
                    self.error_adding_pulse.emit(f"Overlapping pulses in channel {self.tag} due to increasing pulse in iteration: {self.iteration}")
        Collapse=pulse_collapse==True and overlap_fixed_pulses==True
        return Collapse

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
    

    """def Added_Pulses(self,start_time,width,delay_on,delay_off):
        

        
        #the value of the channel   
        #we need to adjust the intervals to account for the delays 
        #including the delays

        end_tail=start_time+width-delay_off
        start_tail=start_time-delay_on
        Adjusted_Interval=[start_tail,end_tail] #specifically for the Pulse_Blaster, these are the intervals that account for the delays to maintain the intended timeframes
        
        pulse_collapse=False
        if delay_off>=width:
            pulse_collapse=True
        overlap_fixed_pulses=False #we define this variable to let the system know when there is an overlap with the fixed pulses
        overlap_variations_pulses=False  #we define this variable to let the system know when there is an overlap with the variations pulses
        if Adjusted_Interval[0]>=0 and pulse_collapse==False: #if the adjustes_interval starts after or on 0=t, to avoid negative time
            Intended_interval=[start_time,start_time+width] #Shown in the graph  
                #now we check if its possible account for the delays in the specific channel (checking if there are any other pulses in the same channel, that overlap with these intervals)
                #allows me to not get an error: List index out of range in the first iteration
            
            if len(self.pb_pulses) > 0 : #if there are other puslse on the same channel we need to check for overlapping, and we also check if the list on the index has a sublist
                for j in range(len(self.pb_pulses)): #we iterate over the pb_pulses in the respective channel, to check for overlapping
                    if j>0:
                        Partially_Left=(self.pb_pulses[j][0]<=end_tail and self.pb_pulses[0]>=start_tail) # if the the new pulse finishes after the start of the previous pulse and starts before the start of the previous pulse
                        Partially_Right=(self.pb_pulses[j][1]<=end_tail and self.pb_pulses[j][1]>=start_tail) # if the new pulse finishes after the end of the previous pulse and starts before the end of the previous pulse
                        Completely_Inside=(self.pb_pulses[j][0]<=start_tail and self.pb_pulses[j][1]>=end_tail) #if the new pulse starts after the start of the previous pulse and finishes before the end of the previous pulse
                        
                        if Partially_Left==True or Partially_Right==True or Completely_Inside==True: #if the pulse is partially, or completely inside the interval the overlap varible becomes true
                            overlap_fixed_pulses=True
                            break #we stop the loop since we already found an overlap
                        
                   
                    #######################################
                    #now we must check for overlapping with any of the pulses that have variations
                    #only if the variation pulse comes before the new pulse (oteriwse we asumme it is accounted for) and only if the pulse is type=0
                if overlap_fixed_pulses==False: #we only check for overlapping on varying pulses if there wasnt overlapping on fixed pulses
                    index_max_end_channel=self.find_indices_first_terms(self.Max_end_type, int(self.tag))
                    if self.contains_sublists(self.Max_end_type)== True: # to check if there are actual variations of iterations in the respective channel
                        self.All_List=self.pulses_ordered_by_time_channels()  
                        self.All_List_PB=self.pulses_ordered_by_time_channels_pb() 
                           
                
                        index_All_list_pb=self.find_indices_first_terms(self.All_List_PB,self.tag)
                            
                        filtered_list_pb=self.All_List_PB[index_All_list_pb]
                            
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
                      
                            if Previous_Pulse!=None:
                                    
                                for i in range(len(self.Max_end_type[index_max_end_channel][Previous_Pulse])):  #list out of range
                                    if i>0:
                                        if len(self.Max_end_type[index_max_end_channel][Previous_Pulse])>1:
                                                
                                            if self.Max_end_type[index_max_end_channel][Previous_Pulse][i][1]>start_tail:
                                                 overlap_variations_pulses=True
    
                    if overlap_fixed_pulses==True: 
                    self.error_adding_pulse.emit(f"Overlapping pulses in channel {self.tag} due to increasing pulse in iteration: {self.iteration}")

                    elif overlap_variations_pulses==True:
                    self.error_adding_pulse.emit(f"Overlapping pulses in channel {self.tag}, due to the increasing iteration on pulse: {Previous_Pulse}")
                else:
                        
                    self.pb_pulses.append(Adjusted_Interval) #we add the adjusted intervals to the sequence, this is for the pulse blaster
                    self.pulses.append(Intended_interval)#we add the intended intervals to the sequence    
                    #self.update_graph_sequence() # this allows us to update the sequence in the graph
                        
                    if self.max_end_time_pb<Adjusted_Interval[1]:
                        self.max_end_time_pb=Adjusted_Interval[1]
                        self.max_end_time=Intended_interval[1]
                    self.pulses=sorted(self.pulses,key=lambda x: x[0])  #we order the pulses by time 
                    self.pb_pulses=sorted(self.pb_pulses,key=lambda x: x[0])  #we order the pulses by time 
                        
                    
                    Pulse=self.pb_pulses.index(Adjusted_Interval)
                        
                        #see if there are other pulses infront of this new pulse
                    ####### UPDATING THE UI IF THE NEW PULSE IS IN BETWEEN OTHER PREVIOUSLY ADDED
                    #we need to add the pulse number to the self.Channel_Pulse_iter
                    if len(self.Channel_Pulse_iter)==1:
                        self.Channel_Pulse_iter.append([1]) #this one simbolizes a pulse_1 we get = [ [channel,[1]] ]
                        #self.Max_end_type.append([1],Intended_interval[1])
                        #self.Max_end_no_iter.append([1])
                            
                            #####################
                            #if we add a pulse in between 2 pulses
                            #lets say i have two pulses and i place one in between, since the Pulse_Box keeps the time order the 2nd pulse will become the new pulse (will this pulse steal the variations from the now 3rd pulse)?Iteration List keeps the second pulse:
                    #elif Pulse<len(self.All_List_PB[All_index_channel_pb])-1: #here we check if there is pulse after the new pulse, the -1 is to substrac the channel element
                    elif Pulse<len(self.pb_pulses):
                        Pulses_to_update= list(range(Pulse,len(self.All_List_PB[All_index_channel_pb]))) # a list with the pulses to update, it was Pulse+1 before
             
                            #if there are, update the variables we add the the new pulse to its position, so all the pulses infront get displaced +1
                        self.Channel_Pulse_iter[Index].insert(Pulse,[Pulse])
                        self.Max_end_type[Index].insert(Pulse,[Pulse])
                        self.Max_end_no_iter[Index].insert(Pulse,[Pulse])
                        self.Iteration_All[Index].insert(Pulse,[Pulse])
                        self.Iteration_All_PB[Index].insert(Pulse,[Pulse])######
                            
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
                        self.Channel_Pulse_iter.append([actual_pulse]) #here we add the actual pulse number to the list
                        #self.Max_end_type[Index].append([actual_pulse])
                        #self.Max_end_no_iter[Index].append([actual_pulse,Intended_interval[1]])
                        #self.Iteration_All[Index].append([actual_pulse])
                        #self.Iteration_All_PB[Index].append([actual_pulse])

            else: #there are no other pulses on this channel
                    #print("No overlapping pulses1")
                self.pb_pulses.append(Adjusted_Interval) #we add the adjusted intervals to the sequence, this is for the pulse blaster
                self.pulses.append(Intended_interval)#we add the intended intervals to the sequence    
                #self.update_graph_sequence() # this allows us to update the sequence in the graph
                #self.All_List=self.pulses_ordered_by_time_channels()  
                #self.All_List_PB=self.pulses_ordered_by_time_channels_pb()
                if self.max_end_time_pb<Adjusted_Interval[1]:
                    self.max_end_time_pb=Adjusted_Interval[1]
                    self.max_end_time=Intended_interval[1]
                    #self.iteration_list_saving=[]
                    #we need to add the pulse number to the self.Channel_Pulse_iter
                
                if len(self.Channel_Pulse_iter)==1:
                        self.Channel_Pulse_iter.append([1]) #this one simbolizes a pulse_1 we get = [ [channel,[1]] ]
                        #self.Max_end_type[Index].append([1])
                        #self.Max_end_no_iter[Index].append([1,Intended_interval[1]])
                        #self.Iteration_All[Index].append([1])
                        #self.Iteration_All_PB[Index].append([1])
                            #print(f"Channel_Pulse_iter: {self.Channel_Pulse_iter}")
                else:
                    index_previous=len(self.Channel_Pulse_iter)-1 # here we get the index of the last pulse on the list Channel_Pulse_iter
                    previous=self.Channel_Pulse_iter[index_previous][0] # we save the previous pulse number
                    actual_pulse= previous + 1
                    self.Channel_Pulse_iter.append([actual_pulse]) #here we add the actual pulse number to the list
                    #self.Max_end_type[Index].append([actual_pulse])
                    #self.Max_end_no_iter[Index].append([actual_pulse,Intended_interval])
                    #self.Iteration_All[Index].append([actual_pulse])
                    #self.Iteration_All_PB[Index].append([actual_pulse])
                    

        elif Adjusted_Interval[0]<0: #if runned the interval fails to start after cero, and gives negative time which is not allowed
            self.error_adding_pulse.emit(f"Adjusting for the delay, gives negative start_time of {Adjusted_Interval[0]} ")
            
        else:
            self.error_adding_pulse.emit(f"cannot adjust for the delay because width={width}<={delay_off}=delay_off")          
        
  
        return [self.pb_pulses] # this is the sequence that will be used for the pulse blaster"""
        
