import serial
import time

# Configuração da porta serial (substitua conforme necessário)
porta_serial = "COM3"  # Windows -> Exemplo: "COM3"
# porta_serial = "/dev/ttyUSB0"  # Linux/Mac -> Exemplo: "/dev/ttyUSB0"
baud_rate = 115200

try:
    esp32 = serial.Serial(porta_serial, baud_rate, timeout=1)
    time.sleep(2)  # Aguarde a estabilização da conexão

    # Enviar ESC (\x1b) para entrar no modo de configuração
    esp32.write(b"\x1b")
    time.sleep(1)  # Espera para garantir que a placa entrou no modo correto
    print("Modo de configuração ativado.")

    def enviar_comando(comando):
        esp32.write((comando + "\n").encode())  # Envia comando para ESP32
        time.sleep(0.5)  # Aguarde resposta
        resposta = esp32.read_all().decode().strip()  # Lê e limpa a resposta
        if resposta:
            print(f"ESP32: {resposta}")
        else:
            print("Nenhuma resposta do ESP32.")

    print("Digite os comandos para o ESP32 (ld st, ld 1, ld 0). Digite 'sair' para encerrar.")
    
    while True:
        cmd = input("> ").strip()
        if cmd.lower() == "sair":
            print("Encerrando conexão...")
            break
        enviar_comando(cmd)

    esp32.close()

except serial.SerialException as e:
    print(f"Erro ao conectar com ESP32: {e}")
