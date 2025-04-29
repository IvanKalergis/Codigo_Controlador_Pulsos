#Clase para añadir canales a la base de datos
from Pulse_class import Pulse

#We chose to leave the channel class to leave the atributtes a channel needs to have in order to be created, and also the requirments it need to serve. 
# Otherwise if it violates the requirments it will let the user know, and it will not be created.
class Channel:


    def __init__(self, tag, color, delay):

        self.channel_tag = tag
        self.channel_color = color
        self.channel_delay = delay

        # For the sequence of pulses
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
    
