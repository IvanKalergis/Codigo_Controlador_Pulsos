#Clase para añadir canales a la base de datos
from Sequence import Sequence
from PySide2.QtCore import QObject , Signal
import copy #we do this to work with the 

#We chose to leave the channel class to leave the atributtes a channel needs to have in order to be created, and also the requirments it need to serve. 
# Otherwise if it violates the requirments it will let the user know, and it will not be created.
class Channel(QObject):

    def __init__(self, tag, label, delay):
        super().__init__()  # Call the base class's __init__ method
        #for each channel
        self.tag = tag #the channel tag (ex: PB0, PB1, etc)
        self.label = label
        self.delay = delay
        self.Sequence_hub=[] #in this list we keep all the sequences creates
        self.error_flag = False  # Flag to track if an error occurred

    error_adding_pulse_channel=Signal(str) 
    def a_sequence(self,start_time,width,function_string,iteration_range,type_change): 
        """
        First we check if the pulse can exist, then we need to check if the user wants to add or edit a pulse, 
        then we add the pulses to the sequences and fuse pulses if needed. Finally we sort the whole self.Sequence_hub
        by order of iteration. 
        """
        if self.delay[1]>=width:
       
            self.error_adding_pulse_channel.emit(f"Pulse delay_off={self.delay[1]}>{width}=width")
            return None
        
        start_time_pb=start_time-self.delay[0]

        if start_time_pb<0:
        
            self.error_adding_pulse_channel.emit(f"Pulses starts with negative time{start_time_pb}")
            return None

        if type_change==0:  #meaning we are adding a new pulse
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
                #calcualte the width for this current iteration
                new_width=width
                if function_string!="":
                    print(f"function string:{function_string}, width:{width}")
                    #vthe variables on the funct_str must be W and i 
                    W=width
                    i=k-iteration_range[0] + 1 # here we need to make for example if iter range [50,55] and i=50 we need x=1, the +1 is for it to start in 1 and not 0
                    new_width=eval(function_string) #varied width
                    print(f"varied_width: {new_width}")
                
                if index==None: #no sequences created
                    sequence_inst=Sequence(k,self.tag)
                    print(f"first sequence on{k} created")
                    sequence_inst.add_pulse(start_time, new_width,self.delay[0],self.delay[1])

                    self.Sequence_hub.append(sequence_inst)
                    #sequence_inst.error_adding_pulse.connect(self.error_adding_pulse_channel.emit)

                    #error: because when i=1 after i=0 a Sequence is created but it's on sequence_hub[0] thus sequence_hub[1] will be out of range
                elif self.Sequence_hub[index].iteration==k: #this means there is already a sequence for this iteration
                    print(f"sequence edited in {k}")
                    self.Sequence_hub[k].add_pulse(start_time, new_width,self.delay[0],self.delay[1]) #we add the pulse to the sequence)
                    
           
            self.Sequence_hub = sorted(self.Sequence_hub, key=lambda sequence: sequence.iteration) # Sort (order) the  self.Sequence_hub list by the `iteration` attribute

        else: #meaning we are editing an existing pulse

            pass #leave this for later
    def a_experiment(self,i):
        """ if we find a sequence for the iteration i we return the values if not we return None"""
        for seq in self.Sequence_hub: 
            if seq.iteration==i: 
                return [seq.pb_pulses,seq.pulses]
        return None
        







