from commands.command import Command
import time

class RFIDWrite(Command):
    def send(self, comm):
        hex_value= "set lrfid 0xFFFFFFFFFF"
        time.sleep(0.1)
        comm.ser.write((hex_value + '\n').encode())
        time.sleep(0.5)
        print("[RFIDWrite]: Sent!")

    def on_validate(self, message_received) -> bool:
        return "sucessful" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[RFIDWrite]: We received a matching line for this command!")
        print("[RFIDWrite]: RFID configured successfully!")
