from PySide2.QtCore import QObject , Signal
from Pulse_class import Pulse
class Experiment(QObject): 
    """
        This class will be focused on having the data sent to the spinapi and will have the necessarry methods to conver the channel tags from decimal to binary.
    """
    def __init__(self,Exp_i_pb,iteration):
        super().__init__()
        self.Exp_i_pb=Exp_i_pb
        self.pb_sequence=[]
        self.iteration=iteration
        self.max_end_time_pb=0
    
    def Prepare_Exp(self):
        if len(self.Exp_i_pb)!=0: 
            self.Order_Exp_i_pb()
        else: #send error message   
            pass
        
        print(f"len(self.pb_sequence):{len(self.pb_sequence)}")
        for pulse in self.pb_sequence: #this is just to show that it0s working it should be taken away later
            print(f"Pulse start:{pulse.start_tail}, end:{pulse.end_tail}, channel:{pulse.channel_binary}")
        

    def Order_Exp_i_pb(self): 
        """ To order the list Exp_pb.  
        Exp_pb=[pb,pb,pb...] were each pb is a list of objetcs for example 
        for one pb=[pulse1, pulse2,..] were each pulse has 3 atributes, 
        one is the start time another other is the end time, and the last 
        atribute is the channel tag, which is a list with the channels of this pulse. """

        
        # Step 1: Flatten all the pulse sequences into one list
        all_pulses = [pulse for pb_pulse_list in self.Exp_i_pb for pulse in pb_pulse_list]
        events = []
        # Step 2: Create events from every pulse's start and end times, per channel
        for pulse in all_pulses:
            for ch in pulse.channel_binary:
                events.append((pulse.start_tail, 0, ch))  # 0 = Start event
                events.append((pulse.end_tail, 1, ch))    # 1 = end event
        # Step 3: Sort events chronologically; starts before ends if times equal
        events.sort()

        self.pb_sequence = []
        active_channels = set()
        last_time = 0  # Start from 0 even if first pulse starts later

        # Step 4: Sweep through time and build new Pulse objects for each interval
        for time, event_type, channel in events:
            # Fill in idle gap if needed
            sorted_channels = sorted(active_channels.copy())######### to transform them into a list
            # If the time has moved forward and some channels are active, record a Pulse
            if last_time < time:# Fill in idle gap if needed with an empty pulse channel 0
                if active_channels:
                    self.pb_sequence.append(Pulse(last_time, time, sorted_channels))
                else:
                    self.pb_sequence.append(Pulse(last_time, time, [0]))  # idle pulse
            # Update active channel set
            if event_type == 0:
                active_channels.add(channel)      # Pulse started
            else:
                active_channels.discard(channel)  # Pulse ended

            # Update the time marker
            last_time = time

        return 
    

  