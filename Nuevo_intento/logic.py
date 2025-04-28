from Channel_class import Channel


class PulseManagerLogic:

    def __init__(self):
        
        self.channels = []

    def add_channel(self, channel_tag, channel_color, channel_delay):
        """
        Adds a channel to the database.
        """
        # Logic to add a channel to the database
        channel = Channel(channel_tag, channel_color, channel_delay)
        self.channels.append(channel)

    def add_pulse_to_channel(self, channel_tag, pulse_delay, pulse_width, pulse_tag):
        """
        Adds a pulse to a channel.
        """
        # Logic to add a pulse to a channel
        for channel in self.channels:
            if channel.channel_tag == channel_tag:
                channel.add_pulse(pulse_delay, pulse_width, pulse_tag)
                break