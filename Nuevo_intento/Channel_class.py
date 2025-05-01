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
        First we check if the pulse overlaps with any of the sequences created, then we need to check if the user wants to add or edit a pulse, then we add the pulses to the sequences
        """
        if self.delay[1]>=width:
       
            self.error_adding_pulse_channel.emit(f"Pulse delay_off={self.delay[1]}>{width}=width")
            return None
        if type_change==0:  #meaning we are adding a new pulse
            #temporary_sequence_hub=copy.deepcopy(self.Sequence_hub)#copy.copy,creates a new object but does not copy the objects within it. copy.deepcopy creates a new object and recursively copies all objects contained within the original object. 
            #we create a temporary sequence hub to check if there is an overlap

            for i in range(iteration_range[0],iteration_range[1]): # we iterate through the iteration range
                print(f"iteration_channel_class: {i}")

                """ now we need to calculate the width of the pulse, by plugging the initial width and the current iteration on the function"""

                #parameter to be replaced in the function

                #calcualte the width for this current iteration
                if function_string!="":
                    #vthe variables on the funct_str must be W and i 
                    W=width
                    i=i
                    width=eval(function_string) #varied width
                    print(f"varied_width: {width}")
                
                if len(self.Sequence_hub)==0: #no sequences created
                    sequence_inst=Sequence(i,self.tag)
                    print("first sequence created")
                    sequence_inst.add_pulse(start_time, width,self.delay[0],self.delay[1])
                    print(f"sequence.add_pulse called")
                    #sequence_inst.error_adding_pulse.connect(self.error_adding_pulse_channel.emit)

                elif self.Sequence_hub[i].iteration==i: #this means there is already a sequence for this iteration
                    print("another sequence created")
                    self.Sequence_hub[i].add_pulse(start_time, width,self.delay[0],self.delay[1]) #we add the pulse to the sequence)
                    print(f"sequence.add_pulse called")
                    #sequence_inst.error_adding_pulse.connect(self.error_adding_pulse_channel.emit) # we recieve the signal form the sequences inst and send it to the logic
                

                if len(self.Sequence_hub)==0:
                    self.Sequence_hub.append(sequence_inst)
                


        else: #meaning we are editing an existing pulse

            pass #leave this for later

    """def handle_error(self, message):
    
        #Slot to handle errors emitted by the Sequence instance.
        
        print(f"Error received: {message}")
        self.error_flag = True  # Set the flag to True when the signal is emitted"""






