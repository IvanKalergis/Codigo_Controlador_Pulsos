from PySide2.QtCore import QObject, Signal, Slot
class MySignalEmitter(QObject):
    # Define a custom signal with an argument of type str
    custom_signal = Signal(str)

    def emit_signal(self, message):
        print("Emitting signal...")
        self.custom_signal.emit(message)  # Emit the signal with a string message
def my_slot(message):
    print(f"Received signal with message: {message}")

# Create an instance of the signal emitter
emitter = MySignalEmitter()

# Connect the signal to the slot
emitter.custom_signal.connect(my_slot)

# Emit the signal
emitter.emit_signal("Hello, PySide2!")