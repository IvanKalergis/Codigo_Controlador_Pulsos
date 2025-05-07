#Clase para añadir canales a la base de datos
from Pulse_class import Pulse
from PySide2.QtCore import QObject , Signal


class Sequence(QObject): #A sequence per iteration ( 1 frame), QObject allows signasl to work
    def __init__(self,iteration,tag,binary):
        super().__init__()  # Call the base class's __init__ method
        self.tag=tag #the channel tag (ex: PB0, PB1, etc)
        self.binary=binary
        self.iteration=iteration #iteration of the sequence, meaning ex: the sequence appears in the 50th iteration of the experiment
        self.pb_pulses=[] # this is the list of the instances of pulses of this particular sequence that will be sent to the pulse blaster (accounting for delays)
        self.pulses=[]  #this is the list of the instances of pulses shown in the simulation.
        #elf.Channel_Pulse_iter=[] # this is the list of the pulses in the channel, it will be used to check for overlapping, WE MIGHT NOT NEED THIS
        self.max_end_time_pb=0 # this is the end time of the sequence, it will be used to check if the pulse blaster is ready to send the next sequence
        self.max_end_time=0
    



    ######   ••••••ADDING A PULSE •••••••
    error_adding_pulse=Signal(str)
    error_signal=Signal()
    def add_pulse(self, start_time,width,delay_on,delay_off): 
        end_tail=start_time+width
        start_tail=start_time
        pulse=Pulse(start_tail,end_tail,self.binary) #without delays

        end_tail=start_time+width-delay_off
        start_tail=start_time-delay_on
        pulse_pb = Pulse(start_tail,end_tail,self.binary) #with delays
        
        status = self.check_pulse_fusion(pulse_pb,pulse) #check if the pulse doensnt overlap
        print(f"Fusion?: {status[2]}, new pulse:{status[0]}")
        if status[2]==True: #if there is no overlap with the fixed pulses
            new_pulse_pb=Pulse(status[0][0],status[0][1],self.binary) #we create a new pulse with the fused intervals
            new_pulse=Pulse(status[1][0],status[1][1],self.binary)
            self.pb_pulses.append(new_pulse_pb)
            self.pulses.append(new_pulse) 
            print(f"pb_pulses added: {new_pulse_pb.start_tail}, {new_pulse_pb.end_tail}")
        else: 
            self.pb_pulses.append(pulse_pb)
            self.pulses.append(pulse) 
            print(f"pb_pulses added: {pulse_pb.start_tail} {pulse_pb.end_tail}")
        #now we need to sort the pb_pulses by the start tail
        self.pb_pulses = sorted(self.pb_pulses, key=lambda pb: pb.start_tail) # Sort (order) the  self.pb_pulses list by the `start_tail` attribute
        self.pulses=sorted(self.pulses, key=lambda pulse: pulse.start_tail)
        for i in range(len(self.pb_pulses)):
            print(f"pb_pulses{i}: [{self.pb_pulses[i].start_tail}, {self.pb_pulses[i].end_tail}]")

    
    def check_pulse_fusion(self,pulse_pb,pulse):
        """
        Here we must aim o see if the corresponding pulse overlaps with any of the the pb_pulses 
        """
        #the value of the channel   
        #we need to adjust the intervals to account for the delays 
        #including the delays
        start_tail_pb=pulse_pb.start_tail
        end_tail_pb=pulse_pb.end_tail
        start_tail=pulse.start_tail
        end_tail=pulse.end_tail
    
        overlap_fixed_pulses=False #we define this variable to let the system know when there is an overlap with the fixed pulses
        #we define this variable to let the system know when there is an overlap with the fixed pulses
    
        if len(self.pb_pulses) > 0 : #if there are other puslse on the same channel we need to check for overlapping, and we also check if the list on the index has a sublist
            global_fusion_pb=[] #we create a list to store the fused pulses, and then check which one is the biggest
            global_fusion=[]
            
            indexes_delete=[] #indexes we will delete later
            for j in range(len(self.pb_pulses)): #we iterate over the pb_pulses in the respective channel, to check for overlapping
                Partially_Left=False
                Partially_Right=False
                Completely_Inside=False
                Completely_Ontop=False
                #print(f"pb_pulses per iteration{j}: {self.pb_pulses[j].start_tail}, {self.pb_pulses[j].end_tail}")
                Partially_Left=(self.pb_pulses[j].start_tail<=end_tail_pb and self.pb_pulses[j].start_tail>start_tail_pb and self.pb_pulses[j].end_tail>=end_tail_pb) # if the the new pulse finishes after the start of the previous pulse and starts before the start of the previous pulse
                Partially_Right=(self.pb_pulses[j].end_tail>=start_tail_pb and self.pb_pulses[j].start_tail<start_tail_pb and self.pb_pulses[j].end_tail<=end_tail_pb) # if the new pulse finishes after the end of the previous pulse and starts before the end of the previous pulse
                Completely_Inside=(self.pb_pulses[j].start_tail<=start_tail_pb and self.pb_pulses[j].end_tail>=end_tail_pb) #if the new pulse starts after the start of the previous pulse and finishes before the end of the previous pulse
                Completely_Ontop=(self.pb_pulses[j].start_tail>=start_tail_pb and self.pb_pulses[j].end_tail<=end_tail_pb)
                """ Our objetvies it to fuse the overlapping pulses, into one pulse"""
                if Partially_Left==True:
                    "we fuse the pulses together "
                    fused_pulse_pb=[start_tail_pb,self.pb_pulses[j].end_tail]
                    fused_pulse=[start_tail,self.pulses[j].end_tail]
                    global_fusion_pb.append(fused_pulse_pb)
                    global_fusion.append(fused_pulse)
                    overlap_fixed_pulses=True
                    print(f"Partially Left")

                elif Partially_Right==True:
                    fused_pulse_pb=[self.pb_pulses[j].start_tail,end_tail_pb]
                    fused_pulse=[self.pulses[j].start_tail,end_tail]
                    global_fusion_pb.append(fused_pulse_pb)
                    global_fusion.append(fused_pulse)
                    overlap_fixed_pulses=True
                    print(f"Partially Right pulse:{fused_pulse}")

                elif Completely_Inside==True:
                    fused_pulse_pb=[self.pb_pulses[j].start_tail,self.pb_pulses[j].end_tail]
                    fused_pulse=[self.pulses[j].start_tail,self.pulses[j].end_tail]
                    global_fusion_pb.append(fused_pulse_pb)
                    global_fusion.append(fused_pulse)
                    overlap_fixed_pulses=True
                    print(f"Completely Inside")

                elif Completely_Ontop==True:
                    fused_pulse_pb=[start_tail_pb,end_tail_pb]
                    fused_pulse=[start_tail,end_tail]
                    global_fusion_pb.append(fused_pulse_pb)
                    global_fusion.append(fused_pulse)
                    overlap_fixed_pulses=True
                    print(f"Completely Ontop")
                    #now we delete the pulses that we fused, so they dont overlap with the new pulse    
                if Partially_Left==True or Partially_Right or Completely_Inside==True or Completely_Ontop:
                    indexes_delete.append(j) 
                    print(f"index to delete{j}")

            if len(global_fusion_pb)>0: #we fuse everything that was fused
                fused_pulse_pb=self.fuse_pulses(global_fusion_pb) # we find the biggest pulse t
                print(f"GLobal_fused_pulse:{global_fusion_pb} and fuse pulses:{fused_pulse_pb}")
                fused_pulse=self.fuse_pulses(global_fusion)
                for index in sorted(indexes_delete, reverse=True): 
                    """
                      we delete the pulses that were already fused from the list
                      is used in the sorted() function to sort the indices in 
                      descending order (from largest to smallest). This ensures that
                        when you delete elements from the list using their indices, you start 
                        with the largest index first. 
                        here we run with a typical 
                    """
                    print(f"pulse to be deleted:{self.pb_pulses[index].start_tail,self.pb_pulses[index].end_tail}")
                    del self.pb_pulses[index]
                    del self.pulses[index]

                return [fused_pulse_pb,fused_pulse,overlap_fixed_pulses]
            
            else:
                return [[start_tail_pb,end_tail_pb],[start_tail,end_tail],overlap_fixed_pulses]
            

        else:
            return [[start_tail_pb,end_tail_pb],[start_tail,end_tail],overlap_fixed_pulses]
                            
                            
    def fuse_pulses(self,pulse_list):
        """
        When 2 or more pulses overlap, we need to fuse them into one pulse, this is done by taking the start and end time
          of the pulses and creating a new pulse with the start and end time of the overlapping pulses
          however there might be multiple overlapping pulses, so we neeed to fuse them all together
        """
        min_value = min(pulse_list, key=lambda x: x[0])[0]
        max_value = max(pulse_list, key=lambda x: x[1])[1]
        return [min_value, max_value]
    


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
    
    ##### •••••• EXPERIMENT
    def experiment(self):
        pass
   