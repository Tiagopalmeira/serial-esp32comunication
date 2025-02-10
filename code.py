import machine
import utime
import ujson
import sys

# Configura o LED embutido da Raspberry Pi Pico
led = machine.Pin(25, machine.Pin.OUT)

def piscar_erro():
    """Pisca o LED três vezes para indicar erro no JSON."""
    for _ in range(3):
        led.value(1)
        utime.sleep(0.25)
        led.value(0)
        utime.sleep(0.25)
    print("Erro no processamento do JSON.")

def processar_json(dados):
    """Processa o JSON e retorna True se 'process' for True, False caso contrário."""
    try:
        json_data = ujson.loads(dados)
        if "process" in json_data and isinstance(json_data["process"], bool):
            print("Chave 'process' encontrada no JSON.")
            return json_data["process"]
        else:
            print("Chave 'process' não encontrada ou não é booleana.")
            return False
    except ValueError:
        print("Erro ao ler o JSON.")
        return None

print("Raspberry Pi Pico iniciada. Aguardando dados JSON...")

while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:  # Verifica se há dados na entrada serial
        received_data = sys.stdin.read().strip()
        print(f"JSON recebido: {received_data}")

        processJson = processar_json(received_data)
        
        if processJson is None:
            piscar_erro()
        else:
            led.value(1 if processJson else 0)
            print(f"LED {'ligado' if processJson else 'apagado'}: JSON processado com sucesso!")

    utime.sleep(1)