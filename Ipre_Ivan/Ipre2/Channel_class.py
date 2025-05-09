#Clase para añadir canales a la base de datos
from Sequence import Sequence
from PySide2.QtCore import QObject , Signal
import copy #we do this to work with the 

#We chose to leave the channel class to leave the atributtes a channel needs to have in order to be created, and also the requirments it need to serve. 
# Otherwise if it violates the requirments it will let the user know, and it will not be created.
class Channel(QObject):

    def __init__(self, tag, binary,label, delay):
        super().__init__()  # Call the base class's __init__ method
        #for each channel
        self.tag = tag #the channel tag (ex: PB0, PB1, etc)
        self.label = label
        self.delay = delay
        self.Sequence_hub=[] #in this list we keep all the sequences creates
        self.error_flag = False  # Flag to track if an error occurred
        self.binary=binary

    error_adding_pulse_channel=Signal(str) 
    def a_sequence(self,start_time,width,function_width,function_start,iteration_range): 
        max_end_time=0
        """
        First we check if the pulse can exist, then we need to check if the user wants to add or edit a pulse, 
        then we add the pulses to the sequences and fuse pulses if needed. Finally we sort the whole self.Sequence_hub
        by order of iteration. 
        """
        #### Checking for errors####
        if self.delay[1]>=width:
       
            self.error_adding_pulse_channel.emit(f"Pulse delay_off={self.delay[1]}>{width}=width")
            return None
        
        start_time_pb=start_time-self.delay[0]

        if start_time_pb<0:
            self.error_adding_pulse_channel.emit(f"Pulses starts with negative time{start_time_pb}")
            return None
        ############################
    
        """ here we need to make for example if iter 
            range [50,55] --> [1,2,3,4,5,6] to plug it into 
            the function for the new width
        """
    
        for k in range(iteration_range[0],iteration_range[1]+1): # we iterate through the iteration range, +1 for it to include the [50,55] last bracket term
            print(f"iteration_channel_class: {k}")

            """ now we need to calculate the width of the pulse, by plugging the initial width and the current 
            iteration on the function."""

            #parameter to be replaced in the function
            """generator expression: enumerate provides both the index and the element while iteratinf throught the list. next() efficiently 
                finds the first match without iterating through the entire list"""
            index = next((j for j, sequence in enumerate(self.Sequence_hub) if sequence.iteration == k), None)
            print(f"index:{index}")
                
            new_width=width
            new_start_time=start_time
            if function_width!="": #the pulse added varies in width (duration)
                #vthe variables on the funct_str must be W and i 
                W=width
                i=k-iteration_range[0] + 1 # here we need to make for example if iter range [50,55] and i=50 we need x=1, the +1 is for it to start in 1 and not 0
                new_width=eval(function_width) #varied width
                print(f"function width:{function_width}, new_width:{new_width}")

                #print(f"varied_width: {new_width}")
            if function_start!="":#the pulse added varies in start_time
                S=start_time
                i=k-iteration_range[0] + 1 
                new_start_time=eval(function_start) #varied width
                print(f"function start_time:{function_start}, new_start_time:{new_start_time}")
            
            new_end_time=new_start_time+new_width
            if new_end_time>max_end_time:
                max_end_time=new_end_time #we do this to keep track of the biggest end time of the added pulse to then compare to the biggest end time of every iteration, this is gonna be eventually used for display

            if index==None: #no sequences created
                sequence_inst=Sequence(k,self.tag,self.binary)
                print(f"first sequence on{k} created")
                sequence_inst.add_pulse(new_start_time, new_width,self.delay[0],self.delay[1])
                self.Sequence_hub.append(sequence_inst)
                #sequence_inst.error_adding_pulse.connect(self.error_adding_pulse_channel.emit)

                    #error: because when i=1 after i=0 a Sequence is created but it's on sequence_hub[0] thus sequence_hub[1] will be out of range
            elif self.Sequence_hub[index].iteration==k: #this means there is already a sequence for this iteration
                print(f"sequence edited in {k}")
                self.Sequence_hub[index].add_pulse(new_start_time, new_width,self.delay[0],self.delay[1]) #we add the pulse to the sequence)
                    
        self.Sequence_hub = sorted(self.Sequence_hub, key=lambda sequence: sequence.iteration) # Sort (order) the  self.Sequence_hub list by the `iteration` attribute
        return max_end_time



    def a_experiment(self,i):
        """ if we find a sequence for the iteration i we return the values if not we return None. 
            This method is mainly to fetch data for the experiment"""
        for seq in self.Sequence_hub: 
            if seq.iteration==i:
                return seq.pb_pulses #since its for the experiment we only need to do pb_  for this
        return None
    
    def a_display(self,i):
        """ if we find a sequence for the iteration i we return the values if not we return None. 
            This method is mainly to fetch data for the display"""
        for seq in self.Sequence_hub: 
            if seq.iteration==i: 
                return seq.pulses #since its for the experiment we only need to do pb_  for this
        return None
        







