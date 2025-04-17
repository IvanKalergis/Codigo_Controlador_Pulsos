from PySide2.QtCore import QObject, Signal

class ListEmitter(QObject):
    # Define a signal that emits a list
    list_signal = Signal(list)

    def emit_list(self):
        data = [1, 2, 3, "Quantum"]
        print("Emitting list signal...")
        self.list_signal.emit(data)  # Emit the signal with a list

# Define a slot to receive the list
def list_slot(received_list):
    print(f"Received list: {received_list}")

# Create an instance of ListEmitter
emitter = ListEmitter()

# Connect the signal to the slot
emitter.list_signal.connect(list_slot)

# Emit the signal
emitter.emit_list()