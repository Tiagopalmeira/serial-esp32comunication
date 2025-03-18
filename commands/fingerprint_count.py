from commands.command import Command
import time

class FPCount(Command):
    def send(self, comm):
        time.sleep(0.1)
        cmd = "fingerprint count\r\n"
        for char in cmd:
            comm.ser.write(char.encode('utf-8'))
            time.sleep(0.01)
        comm.ser.flush()
        time.sleep(0.1)
        print("[FPCount]: Sent!")

    def on_validate(self, message_received) -> bool:
        return "count" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[FPCount]: We received a matching line for this command!")
        print("[FPCount]: FP Count issued successfully!")
