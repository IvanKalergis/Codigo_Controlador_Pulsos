class Pulse:
    def __init__(self, start, end, channel_tag):
        self.start = start
        self.end = end
        self.channel_tag = channel_tag

    def __repr__(self):
        return f"Pulse({self.start}, {self.end}, {sorted(self.channel_tag)})"


def split_all_sequences_with_idle(exp_pb):
    # Flatten all pulses from all sequences
    all_pulses = [pulse for sequence in exp_pb for pulse in sequence]

    # Create event list: (time, type, channel)
    events = []
    for pulse in all_pulses:
        for ch in pulse.channel_tag:
            events.append((pulse.start, 0, ch))  # 0 = start
            events.append((pulse.end, 1, ch))    # 1 = end

    # Sort all events: first by time, then by type (start before end)
    events.sort()

    result = []
    active_channels = set()
    last_time = 0  # Start from 0 even if first pulse starts later

    for time, event_type, channel in events:
        # Fill in idle gap if needed
        sorted_channels = sorted(active_channels.copy())######### to transform them
        if last_time < time:
            if active_channels:
                result.append(Pulse(last_time, time, sorted_channels))
            else:
                result.append(Pulse(last_time, time, [0]))  # idle pulse

        # Update active channels
        if event_type == 0:
            active_channels.add(channel)
        else:
            active_channels.discard(channel)

        last_time = time

    return result
seq1 = [Pulse(2, 4, [1])]
seq2 = [Pulse(6, 8, [2])]
Exp_pb = [seq1, seq2]

flattened = split_all_sequences_with_idle(Exp_pb)
for p in flattened:
    print(p)