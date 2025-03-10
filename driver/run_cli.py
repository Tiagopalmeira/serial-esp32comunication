import serial
import time
import keyboard

def estabelecer_comunicacao_serial(porta, baud_rate):
    try:
        # Abrir a porta serial
        ser = serial.Serial(porta, baud_rate)
        print("Comunicação serial estabelecida com sucesso!")
        return ser
    except Exception as e:
        print(f"Erro ao estabelecer a comunicação: {e}")
        return None

def ativar_modo_debug(ser):
    print("Pressione ESC para ativar o modo de debug na placa ESP32.")
    
    # Aguardar a tecla ESC ser pressionada
    while True:
        if keyboard.is_pressed('esc'):
            print("Tecla ESC pressionada. Enviando comando para ativar modo de debug na placa...")
            ser.write(bytes([27]))  # Envia o código ASCII 27, que representa a tecla ESC
            break
        time.sleep(0.1)  # Pequeno atraso para evitar uso excessivo de CPU

def aguardar_comandos_e_enviar(ser):
    print("Modo de debug ativado. Agora, você pode enviar comandos para a placa.")
    
    while True:
        comando = input("Digite o comando (exemplo: 'led on' ou 'led off'): ")
        
        # Enviar o comando para a placa
        if comando:
            ser.write((comando + "\n").encode('utf-8'))  # Envia o comando para a placa
            print(f"Comando enviado: {comando}")

            # Espera por resposta da placa (opcional)
            time.sleep(1)
            if ser.in_waiting > 0:
                resposta = ser.read(ser.in_waiting)
                print("Resposta da placa:", resposta.decode('utf-8'))

def main():
    # Configurações da porta serial
    porta = '/dev/ttyACM0'  # Altere para a porta serial correta no seu sistema
    baud_rate = 115200       # Taxa de transmissão (baud rate)

    # Estabelecer a comunicação serial
    ser = estabelecer_comunicacao_serial(porta, baud_rate)

    if ser:
        # Ativar modo de debug
        ativar_modo_debug(ser)

        # Aguardar comandos e enviar para a placa
        aguardar_comandos_e_enviar(ser)

        # Fechar a porta serial após o uso
        ser.close()

# Executar o programa
if __name__ == "__main__":
    main()
