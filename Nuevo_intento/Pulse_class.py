#Clase para añadir pulsos a la secuencia de pulsos

#Basically everything a pulse needs to have in order to be created, and also the requirments it need to serve in orther to function correctly
class Pulse:


    def __init__(self,start_tail,end_tail): #we dont need the delay, right??
        self.start_tail=start_tail
        self.end_tail=end_tail

#later we will have to add some methods for varying a pulse's width.