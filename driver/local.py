import serial
import json
import time
import usb.core
import usb.util

# Configuração da porta serial (ajuste conforme necessário)
PORT = 'COM4'
BAUDRATE = 115200

# Definição dos dispositivos autorizados (VID e PID)
AUTHORIZED_DEVICES = [
    {"vid": 0x1a86, "pid": 0x55d4},  #exemplo aleatório
    {"vid": 0x1a2c, "pid": 0x45ea},  #esp32
]


def check_authorized_device():
    """Verifica se um dispositivo USB conectado é autorizado."""
    devices = usb.core.find(find_all=True)
    for device in devices:
        vid = device.idVendor
        pid = device.idProduct

        for auth_device in AUTHORIZED_DEVICES:
            if vid == auth_device["vid"] and pid == auth_device["pid"]:
                print(f"Dispositivo autorizado encontrado: VID={
                      hex(vid)}, PID={hex(pid)}")
                return True
    print("Dispositivo não autorizado encontrado.")
    return False


def send_json_to_esp32(data):
    """Serializa e envia os dados JSON para a ESP32 via porta serial."""
    try:
        # Verifica se a porta USB é autorizada
        if not check_authorized_device():
            print("Dispositivo USB não autorizado. Abortando comunicação.")
            return

        # Abrindo a conexão serial com a ESP32
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            # Serializa os dados para JSON
            json_data = json.dumps(data)
            # Envia os dados para a ESP32
            ser.write(json_data.encode('utf-8'))
            ser.flush()  # Garante que os dados sejam enviados
            print(f"Enviado para ESP32: {json_data}")

            # Aguarda a ESP32 processar a mensagem
            time.sleep(2)

            # Lê a resposta da ESP32
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                print(f"Resposta da ESP32: {response}")
    except Exception as e:
        print(f"Erro ao se comunicar com a ESP32: {e}")



data_to_send = {
    "process": True
}

# Enviar os dados para a ESP32
send_json_to_esp32(data_to_send)
