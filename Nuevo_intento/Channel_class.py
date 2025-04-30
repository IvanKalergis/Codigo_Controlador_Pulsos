#Clase para añadir canales a la base de datos
from Sequence import Sequence
from PySide2.QtCore import QObject , Signal
import copy #we do this to work with the 

#We chose to leave the channel class to leave the atributtes a channel needs to have in order to be created, and also the requirments it need to serve. 
# Otherwise if it violates the requirments it will let the user know, and it will not be created.
class Channel:

    def __init__(self, tag, label, delay):
        #for each channel
        self.tag = tag #the channel tag (ex: PB0, PB1, etc)
        self.label = label
        self.delay = delay
        self.Sequence_hub=[] #in this list we keep all the sequences creates

    error_adding_pulse_channel=Signal(str) 
    def a_sequence(self,start_time,width,function_string,iteration_range,type_change): 
        """
        First we check if the pulse overlaps with any of the sequences created, then we need to check if the user wants to add or edit a pulse, then we add the pulses to the sequences
        """
        if type_change==0:  #meaning we are adding a new pulse
            temporary_sequence_hub=self.Sequence_hub

            for i in range(iteration_range[0],iteration_range[1]): # we iterate through the iteration range

                """ now we need to calculate the width of the pulse, by plugging the initial width and the current iteration on the function"""

                #parameter to be replaced in the function
                W=width
                i=i
                #calcualte the width for this current iteration
                varied_width=eval(function_string)
                print(f"varied_width: {varied_width}")
                if len(self.Sequence_hub)==0: #no sequences created
                    sequence_inst=Sequence(i,self.tag)
                    sequence_inst.add_pulse(start_time, varied_width,self.delay[0],self.delay[1])
                    sequence_inst.error_adding_pulse.connect(self.error_adding_pulse_channel.emit)

                elif self.Sequence_hub[i].iteration==i: #this means there is already a sequence for this iteration
                    sequence_inst=self.Sequence_hub[i]
                    sequence_inst.add_pulse(start_time, varied_width,self.delay[0],self.delay[1]) #we add the pulse to the sequence)
                    sequence_inst.error_adding_pulse.connect(self.error_adding_pulse_channel.emit) # we recieve the signal form the sequences inst and send it to the logic

                temporary_sequence_hub.append(sequence_inst)

        else: #meaning we are editing an existing pulse

            pass #leave this for later






