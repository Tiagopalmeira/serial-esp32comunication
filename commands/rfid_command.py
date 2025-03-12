from commands.command import Command

class RFIDWrite(Command):
    def send(self, comm):
        comm.ser.write(("lfrid enable\n").encode('utf-8'))
        comm.ser.write(("lrfid set 0xFFFFFFFFF\n").encode('utf-8'))

    def on_validate(self, message_received) -> bool:
        return "successful" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[RFIDWrite]: RFID configurado com sucesso!")
