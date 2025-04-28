#Clase para añadir pulsos a la secuencia de pulsos

#Basically everything a pulse needs to have in order to be created, and also the requirments it need to serve in orther to function correctly
class Pulse:


    def __init__(self, pulse_delay, pulse_width, pulse_tag):

        self.pulse_delay = pulse_delay
        self.pulse_width = pulse_width
        self.pulse_tag = pulse_tag