from PySide2.QtCore import QObject , Signal
import pyqtgraph as pg
class Frame(QObject):
    """
    This class corresponds to the architecture of a frame
      of the graph for a particular iteration. It recieves 
      max_end time of al the iterations, because otherwise 
      as you create frames the pulses to the user might seem 
      to change even though they are fixed because of having each 
      frame a different end time. 
    """
    def __init__(self,channel_tags_colors,sequences,iteration,max_end):
        super().__init__()
        self.channel_tags_colors=channel_tags_colors
        self.sequences=sequences
        self.iteration=iteration
        self.PlotSequences=[]
        
    """def Display_Frame(self):
        for sequence_channel in self.sequences:
        
        pass"""
    def Display_Frame(self):
        """
        Plots sequences of pulses as stacked Heaviside (step) functions
        into the provided pyqtgraph PlotWidget.

        Parameters:
        - graphWidget: a pg.PlotWidget instance (e.g. self.ui.graphWidget)
        - sequences: list of lists of Pulse objects, one list per channel
        """
        # First, find the global end time (latest end time across all pulses)
        global_end = 0
        for seq in self.sequences:
            for pulse in seq:
                if pulse.end_tail > global_end:
                    global_end = pulse.end_tail
        for i, seq in enumerate(self.sequences):
            x = []  # x-axis values (time)
            y = []  # y-axis values (level for Heaviside + offset)

            offset = 2 * i  # vertical space between channels

            # Sort the pulses in this channel by start time
            seq = sorted(seq, key=lambda p: p.start_tail) #this is trivial they should already be sorted

            last_end = 0  # Tracks the end of the last pulse to detect gaps

            for pulse in seq:
                # If there is a gap before the next pulse, draw a flat line at 0
                if pulse.start_tail > last_end:
                    x.extend([last_end, pulse.start_tail])
                    y.extend([offset, offset])  # Flat baseline

                # Rising edge: step up at start
                x.append(pulse.start_tail)
                y.append(offset)

                x.append(pulse.start_tail)
                y.append(offset + 1)

                # High level: flat line from start to end
                x.append(pulse.end_tail)
                y.append(offset + 1)

                # Falling edge: step down at end
                x.append(pulse.end_tail)
                #y.append(offset)

                last_end = pulse.end_tail  # Update the last end for gap checking
            # If the last pulse ends before the global end, extend the flat line
            if last_end < global_end:
                x.extend([last_end, global_end])
                y.extend([offset, offset])
            # Optionally, draw a flat tail after the last pulse
            #x.append(last_end + 1)
            #y.append(offset)
        
            # Create a PlotDataItem with step mode to mimic Heaviside function
            plot_item = pg.PlotDataItem(
                x, y,
                stepMode=True,       # Important for square wave behavior
                pen=pg.mkPen(width=2)  # Line thickness
            )

            # Add the pulse trace to frame list 
            self.PlotSequences.append(plot_item)
            #graphWidget.addItem(plot_item)
        