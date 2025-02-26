import serial

def ler_porta_serial(porta: str, baud_rate: int = 9600, timeout: float = 1) -> None:
    """
    Abre a porta serial e lê continuamente os dados enviados, exibindo-os no console.
    
    :param porta: Caminho da porta serial, ex: '/dev/ttyUSB0' ou 'COM3'.
    :param baud_rate: Taxa de transmissão (baud rate). Padrão: 9600.
    :param timeout: Tempo de espera para leitura. Padrão: 1 segundo.
    """
    try:
        with serial.Serial(porta, baud_rate, timeout=timeout) as ser:
            print(f"Abrindo a porta {porta} com baud rate {baud_rate}...")
            while True:
                # Verifica se há dados disponíveis
                if ser.in_waiting:
                    # Lê até a próxima quebra de linha
                    linha = ser.readline()
                    # Decodifica para string e remove espaços em branco
                    dados = linha.decode('utf-8', errors='replace').strip()
                    print("Dados recebidos:", dados)
    except serial.SerialException as e:
        print(f"Erro ao acessar a porta serial: {e}")
    except KeyboardInterrupt:
        print("Leitura interrompida pelo usuário.")

if __name__ == "__main__":
    # Altere 'porta_serial' para o caminho da sua porta. Ex: '/dev/ttyUSB0' no Linux ou 'COM3' no Windows.
    porta_serial = 'COM4'
    baud = 9600
    ler_porta_serial(porta_serial, baud)
