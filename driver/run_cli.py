import serial
import time


porta_serial = "COM3"  
# porta_serial = "/dev/ttyUSB0"  
baud_rate = 115200

try:
    esp32 = serial.Serial(porta_serial, baud_rate, timeout=1)
    time.sleep(2)  
    print("Conexão serial iniciada.")
    print("Pressione 'ESC' para entrar no modo de configuração.")

    while True:
        tecla = input("> ")  
        if tecla == "\x1b": 
            esp32.write(b"\x1b") 
            time.sleep(1)
            print("Modo de configuração ativado.")
            break
        else:
            print("Pressione 'ESC' para continuar.")

    print("Modo debug iniciado. Agora você pode enviar comandos para o ESP32.")
    print("Digite os comandos ou 'sair' para encerrar.")

    def enviar_comando(comando):
        esp32.write((comando + "\n").encode()) 
        time.sleep(0.5) 
        resposta = esp32.read_all().decode().strip() 
        if resposta:
            print(f"ESP32: {resposta}")
        else:
            print("Nenhuma resposta do ESP32.")

    while True:
        cmd = input("> ").strip()
        if cmd.lower() == "sair":
            print("Encerrando conexão...")
            break
        enviar_comando(cmd)

    esp32.close()

except serial.SerialException as e:
    print(f"Erro ao conectar com ESP32: {e}")
