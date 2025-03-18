from core.communication import Communication
from commands.rfid_command import RFIDWrite
from commands.fingerprint_count import FPCount

class ITDMInterface:
    def __init__(self, comm: Communication):
        self.comm = comm

    def default_callback(self, message):
        print(f"[ITDM]: {message}")

    def WriteRFID(self):
        print("[ITDM]: Enviando comando RFID...")
        self.comm.send(RFIDCommand())
    
    def CountFP(self):
        print("[ITDM]: Enviando comando FP Count")
        self.comm.send(FPCount())
