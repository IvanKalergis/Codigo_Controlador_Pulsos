#Clase para añadir canales a la base de datos
from Pulse_class import Pulse
from PySide2.QtCore import QObject , Signal

#We chose to leave the channel class to leave the atributtes a channel needs to have in order to be created, and also the requirments it need to serve. 
# Otherwise if it violates the requirments it will let the user know, and it will not be created.
class Channel:


    def __init__(self, tag, label, delay):
        #for each channel
        self.tag = tag #the channel tag (ex: PB0, PB1, etc)
        self.label = label
        self.delay = delay
