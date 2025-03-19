from commands.command import Command
import time

class RFIDWrite(Command):
    def send(self, comm):
        time.sleep(0.1)
        cmd = "lfrfid set 0xFFFFFFFFFF \r\n"
        for char in cmd:
            comm.ser.write(char.encode('utf-8'))
            time.sleep(0.01)
        time.sleep(0.1)
        print("[RFIDWrite]: Sent!")

    def on_validate(self, message_received) -> bool:
        return "sucessful" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[RFIDWrite]: We received a matching line for this command!")
        print("[RFIDWrite]: RFID configured successfully!")
