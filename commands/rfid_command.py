from commands.command import Command
import time

class RFIDWrite(Command):
    def send(self, comm):
        time.sleep(0.1)
        comm.ser.write(b"lrfid set 0xFFFFFFFFF\r\n")
        time.sleep(0.1)
        print("[RFIDWrite]: Sent!")

    def on_validate(self, message_received) -> bool:
        return "sucessful" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[RFIDWrite]: We received a matching line for this command!")
        print("[RFIDWrite]: RFID configured successfully!")
