from commands.command import Command
import time


class FPUnenroll(Command):
    def send(self, comm):
        time.sleep(0.1)
        
        cmd = "fingerprint unenroll all\r\n"
        for char in cmd:
            comm.ser.write(char.encode('utf-8'))
            time.sleep(0.01)

        time.sleep(1)
            



    def on_validate(self, message_received) -> bool:
        return "successful" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[Enroll Begin Local]: We received a matching line for this command!")


class FPEnrollBegin(Command):
    def send(self, comm):
        time.sleep(0.1)

        cmd = "fingerprint enroll begin\r\n"
        for char in cmd:
            comm.ser.write(char.encode('utf-8'))
            time.sleep(0.01)
    
    time.sleep(1)



    def on_validate(self, message_received) -> bool:
        return "successful" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[Enroll Begin Local]: We received a matching line for this command!")

class FPEnrollSubscribe(Command):
    def send(self, comm):
        time.sleep(0.1)

        cmd = "fingerprint subscribe\r\n"
        for char in cmd:
            comm.ser.write(char.encode('utf-8'))
            time.sleep(0.01)

        time.sleep(1)
               
    def on_validate(self, message_received) -> bool:
        return "successful" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[Enroll Subscribe Local]: We received a matching line for this command!")

class FPEnrollCapture(Command):
    enrolledCount = int(0)

    def send(self, comm):
        time.sleep(1.0)

        cmd = "fingerprint enroll capture\r\n"
        for char in cmd:
            comm.ser.write(char.encode('utf-8'))
            time.sleep(0.01)
        
        time.sleep(1)
               
    def on_validate(self, message_received) -> bool:
        return "successful" in message_received.lower()

    def on_receive(self, comm, message_received):      
        print("[Enroll Capture Local]: We received a matching line for this command!")


class FPEnrollFinalize(Command):
    def send(self, comm):
        time.sleep(0.1)

        cmd = "fingerprint enroll finalize 1\r\n"
        for char in cmd:
            comm.ser.write(char.encode('utf-8'))
            time.sleep(0.01)
        
        time.sleep(1)
               
    def on_validate(self, message_received) -> bool:
        return "successful" in message_received.lower()

    def on_receive(self, comm, message_received):
        print("[Enroll Subscribe Local]: We received a matching line for this command!")