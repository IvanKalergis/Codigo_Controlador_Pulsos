from PySide2.QtCore import QObject, Signal, Slot
class MultiArgEmitter(QObject):
    multi_signal = Signal(int, str)

    def emit_signal(self):
        self.multi_signal.emit(42, "Quantum teleportation!")

def multi_slot(number, text):
    print(f"Received number: {number}, message: {text}")

# Example usage
emitter = MultiArgEmitter()
emitter.multi_signal.connect(multi_slot)
emitter.emit_signal()