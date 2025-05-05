# === Define the Pulse class ===
class Pulse:
    def __init__(self, start, end, channel_tag):
        self.start = start
        self.end = end
        self.channel_tag = channel_tag

    def __repr__(self):
        return f"Pulse({self.start}, {self.end}, {sorted(self.channel_tag)})"

# === Define the function that processes sequences of pulses ===
def split_all_sequences(exp_pb):
    all_pulses = [pulse for sequence in exp_pb for pulse in sequence]

    events = []
    for pulse in all_pulses:
        for ch in pulse.channel_tag:
            events.append((pulse.start, 0, ch))
            events.append((pulse.end, 1, ch))

    events.sort()
    result = []
    active_channels = set()
    last_time = None

    for time, event_type, channel in events:
        if last_time is not None and time != last_time and active_channels:
            result.append(Pulse(last_time, time, active_channels.copy()))

        if event_type == 0:
            active_channels.add(channel)
        else:
            active_channels.discard(channel)

        last_time = time

    return result

# === Define example sequences ===
seq1 = [Pulse(1, 10, [1])]
seq2 = [Pulse(5, 8, [2])]
seq3 = [Pulse(6, 12, [3])]
Exp_pb = [seq1, seq2, seq3]

# === Run the function ===
flattened_pulses = split_all_sequences(Exp_pb)

# === Print the result ===
print("Split pulses timeline:")
for p in flattened_pulses:
    print(p)