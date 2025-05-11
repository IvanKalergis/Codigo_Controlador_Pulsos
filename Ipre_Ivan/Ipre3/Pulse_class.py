#Clase para añadir pulsos a la secuencia de pulsos

#Basically everything a pulse needs to have in order to be created, and also the requirments it need to serve in orther to function correctly
class Pulse:


    def __init__(self,start_tail,end_tail,channel_binary): #we dont need the delay, right??
        self.start_tail=start_tail
        self.end_tail=end_tail
        #self.channel_tag=[channel_tag] #we make it a list because later when creating the experiment, we might have 2 pulses from different channels that start at the same time.
        self.channel_binary=[channel_binary] #might be better to recieve the value fo the channel in binary, because later the convertion will take a lot of time

