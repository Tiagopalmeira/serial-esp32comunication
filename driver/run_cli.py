import serial
import time
import sys
import termios
import tty


porta_serial = "/dev/ttyUSB0"  
# porta_serial = "COM3"  # Windows (caso use no Windows)
baud_rate = 115200

def ler_tecla():
    """ Captura uma única tecla pressionada no terminal. """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        tecla = sys.stdin.read(1) 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return tecla

try:
    esp32 = serial.Serial(porta_serial, baud_rate, timeout=1)
    time.sleep(2) 
    print("Conexão serial iniciada.")
    print("Pressione 'ESC' para entrar no modo de configuração.")

    while True:
        tecla = ler_tecla()
        if tecla == "\x1b":  
            esp32.write(b"\x1b") 
            time.sleep(1)
            print("\nModo de configuração ativado.")
            break
        else:
            print("\nPressione 'ESC' para continuar.")

    print("Modo debug iniciado. Agora você pode enviar comandos para o ESP32.")
    print("Digite os comandos (ld st, ld 1, ld 0) ou 'sair' para encerrar.")

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
