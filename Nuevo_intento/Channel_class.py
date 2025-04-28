#Clase para añadir canales a la base de datos
class Channel:
    def __init__(self, channel_tag, channel_color, channel_delay, sequence):
        self.channel_tag =channel_tag
        self.channel_color = channel_color
        self.channel_delay = channel_delay
        self.sequence = sequence
