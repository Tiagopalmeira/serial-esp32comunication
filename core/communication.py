import serial
import time
import threading
import re

def decode_and_split(data_bytes):
    # Decodificar os bytes em uma string e dividir pelas quebras de linha.
    text = data_bytes.decode('utf-8', errors='ignore')
    lines = re.split(r'[\r\n]+', text)
    return [l.strip() for l in lines if l.strip()]

class Communication:
    def __init__(self, port, baud_rate, callback):
        # Iniciando as variáveis de configuração, callback e serial.
        self.port = port
        self.baud_rate = baud_rate
        self.callback = callback
        self.ser = None
        try:
            # Tentando abrir a porta serial
            self.ser = serial.Serial(port, baud_rate, timeout=0.1)
        except serial.SerialException as e:
            # Se não conseguir abrir a porta, mostramos um erro claro
            print(f"[STM32]: Erro ao abrir a porta serial: {e}")
            self.ser = None
        self.running = False
        self.listening_thread = None
        self.pending_command = None
        self.lock = threading.Lock()  # Adicionamos um lock para proteger o acesso ao comando pendente.

    @property
    def is_connected(self):
        # Verifica se a conexão serial está ativa
        return self.ser is not None

    def start_listening(self):
        # Inicia a escuta da porta serial se estiver conectada
        if not self.is_connected:
            print("[STM32]: Não há conexão serial.")
            return
        self.running = True
        self.listening_thread = threading.Thread(
            target=self.listening_loop, daemon=True
        )
        self.listening_thread.start()

    def listening_loop(self):
        # Loop responsável por ler a porta serial continuamente
        buffer_line = b""  # Acumulador de bytes lidos
        stacked_lines = []  # Acumulador de linhas completas
        while self.running:
            try:
                read_count = self.ser.in_waiting  # Verifica se há dados para ler
                if read_count:
                    chunk = self.ser.read(read_count)
                    buffer_line += chunk  # Adiciona ao buffer
                else:
                    if buffer_line:
                        # Quando não há novos dados, tentamos processar o buffer
                        lines_found = decode_and_split(buffer_line)
                        buffer_line = b""  # Reseta o buffer após processar
                        stacked_lines.extend(lines_found)  # Adiciona as linhas completas

                    # Se há linhas acumuladas, processamos elas
                    if stacked_lines:
                        multiline_str = "\n".join(stacked_lines)
                        # Chama o callback com as linhas recebidas
                        self.callback(multiline_str)

                        # Processamos os comandos, se houver algum pendente
                        with self.lock:  # Bloqueamos para evitar problemas de concorrência
                            for line_decoded in stacked_lines:
                                if self.pending_command and self.pending_command.on_validate(line_decoded):
                                    self.pending_command.on_receive(self, line_decoded)
                                    self.pending_command = None

                        stacked_lines.clear()  # Limpa as linhas após o processamento

                time.sleep(0.03)  # Espera um pouco antes de ler novamente
            except Exception as e:
                print(f"[STM32]: Erro ao ler os dados: {e}")
                time.sleep(0.1)  # Espera antes de tentar novamente

    def send(self, command_obj):
        # Envia um comando se a conexão estiver ativa
        if not self.is_connected:
            print("[STM32]: Não é possível enviar comando, sem conexão serial.")
            return
        with self.lock:  # Bloqueio para proteger o acesso ao comando pendente
            self.pending_command = command_obj
        try:
            command_obj.send(self)  # Envia o comando para a porta serial
            print(f"[STM32]: Comando enviado: {command_obj.__class__.__name__}")
        except Exception as e:
            print(f"[STM32]: Erro ao enviar comando: {e}")

    def close(self):
        # Fecha a conexão serial de forma segura
        self.running = False
        if self.ser:
            # Espera a thread de leitura terminar antes de fechar
            if self.listening_thread and self.listening_thread.is_alive():
                self.listening_thread.join()
            self.ser.close()
            print("[STM32]: Conexão serial fechada com sucesso.")

    def reconnect(self):
        # Método adicional para tentar reconectar a porta serial, se necessário.
        if self.ser and not self.ser.is_open:
            try:
                self.ser.open()
                print("[STM32]: Porta serial reconectada.")
            except serial.SerialException as e:
                print(f"[STM32]: Erro ao tentar reconectar: {e}")
