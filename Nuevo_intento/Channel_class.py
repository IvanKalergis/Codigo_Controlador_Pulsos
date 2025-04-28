#Clase para añadir canales a la base de datos
from Sequence_class import Sequence
from Pulse_class import Pulse


class Channel:


    def __init__(self, tag, color, delay_on, delay_off):

        self.channel_tag = tag
        self.channel_color = color
        self.channel_delay = delay_on
        self.channel_delay_off = delay_off

        # For the sequence of pulses
        self.pulse_list = []

    def add_pulse(self, pulse_delay, pulse_width, pulse_tag):

        pulse = Pulse(pulse_delay, pulse_width, pulse_tag)
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
        for pulse in self.pulse_list:
            display_list.append((pulse.pulse_delay, pulse.pulse_width, pulse.pulse_color, pulse.pulse_tag))
        return display_list
    
