import serial
import time
import threading
import re

def decode_and_split(data_bytes):
    text = data_bytes.decode('utf-8', errors='ignore')
    lines = re.split(r'[\r\n]+', text)
    return [l.strip() for l in lines if l.strip()]

class Communication:
    def __init__(self, port, baud_rate, callback):
        self.port = port
        self.baud_rate = baud_rate
        self.callback = callback
        self.ser = None
        try:
            self.ser = serial.Serial(port, baud_rate, timeout=0.1)
        except serial.SerialException as e:
            print(f"[STM32]: Error opening serial port: {e}")
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
        self.listening_thread = threading.Thread(
            target=self.listening_loop, daemon=True
        )
        self.listening_thread.start()

    def listening_loop(self):
        buffer_line = b""
        stacked_lines = []
        while self.running:
            try:
                # Lê tudo que estiver disponível no momento
                read_count = self.ser.in_waiting
                if read_count:
                    chunk = self.ser.read(read_count)
                    buffer_line += chunk
                else:
                    # Se não chegou nada novo, é um bom momento para “dar flush”.
                    if buffer_line:
                        # Extrai as linhas completas do buffer
                        lines_found = decode_and_split(buffer_line)
                        buffer_line = b""
                        # Empilha as linhas extraídas
                        stacked_lines.extend(lines_found)

                    # Se há linhas acumuladas, imprimimos de uma só vez
                    if stacked_lines:
                        # Monta um único bloco com quebras de linha
                        multiline_str = "\n".join(stacked_lines)
                        # Faz o print "empilhado"
                        self.callback(multiline_str)

                        # Agora, para cada linha individual,
                        # tentamos validar o comando pendente.
                        for line_decoded in stacked_lines:
                            if (self.pending_command and
                                self.pending_command.on_validate(line_decoded)):
                                self.pending_command.on_receive(self, line_decoded)
                                self.pending_command = None

                        # Limpamos a pilha após imprimir e validar
                        stacked_lines.clear()

                time.sleep(0.03)

            except Exception as e:
                print(f"[STM32]: Error reading data: {e}")
                time.sleep(0.1)

    def send(self, command_obj):
        if not self.is_connected:
            print("[STM32]: Cannot send command, no serial connection.")
            return
        self.pending_command = command_obj
        try:
            command_obj.send(self)
            print(f"[STM32]: Command sent: {command_obj.__class__.__name__}")
        except Exception as e:
            print(f"[STM32]: Error sending command: {e}")

    def close(self):
        self.running = False
        if self.ser:
            self.ser.close()
