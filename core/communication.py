import serial
import time
import threading

class Communication:
    def __init__(self, port, baud_rate, callback):
        self.port = port
        self.baud_rate = baud_rate
        self.callback = callback
        try:
            self.ser = serial.Serial(port, baud_rate, timeout=1)
        except serial.SerialException as e:
            print(f"[STM32]: Erro ao abrir a porta serial: {e}")
            self.ser = None
        self.running = False
        self.listening_thread = None
        self.pending_command = None

    @property
    def is_connected(self):
        return self.ser is not None

    def start_listening(self):
        if not self.is_connected:
            return
        self.running = True
        self.listening_thread = threading.Thread(target=self.listening_loop, daemon=True)
        self.listening_thread.start()

    def listening_loop(self):
        while self.running:
            if self.ser.in_waiting:
                try:
                    data = self.ser.read(self.ser.in_waiting).decode('utf-8').strip()
                    if data:
                        self.callback(data)
                        if self.pending_command is not None:
                            if self.pending_command.on_validate(data):
                                self.pending_command.on_receive(self, data)
                                self.pending_command = None
                except Exception as e:
                    print(f"[STM32]: Erro ao ler dados: {e}")
            time.sleep(0.25)

    def send(self, command_obj):
        if not self.is_connected:
            print("[STM32]: Não é possível enviar comando, conexão não estabelecida.")
            return
        self.pending_command = command_obj
        try:
            command_obj.send(self)
            print(f"[STM32]: Comando enviado: {command_obj.__class__.__name__}")
        except Exception as e:
            print(f"[STM32]: Erro ao enviar comando: {e}")

    def close(self):
        self.running = False
        if self.ser:
            self.ser.close()
