from core.terminalui import TerminalUI
from core.communication import Communication
from commands.rfid_command import RFIDWrite
from itdm_interface import ITDMInterface
import threading

def main():
    ui = TerminalUI()
    interactive_mode_event = threading.Event()

    def stm32_callback(message):
        ui.print_message(message, tag="STM32")
        if "modo interativo ativado" in message.lower():
            interactive_mode_event.set()

    def create_connection():
        return Communication(port="COM7", baud_rate=115200, callback=stm32_callback)

    comm = create_connection()

    if comm.is_connected:
        comm.start_listening()
        ui.print_status("Conexão serial estabelecida com sucesso.", success=True)
        ui.print_message("Aguardando que o CLI da STM32 entre no modo interativo (pressione ESC no CLI da STM32)...", tag="API UI")
        interactive_mode_event.clear()
        interactive_mode_event.wait()
        ui.print_status("Modo interativo ativado.", success=True)
    else:
        ui.print_status("Erro: Conexão serial não estabelecida.", success=False)

    while True:
        if not comm.is_connected:
            ui.print_message("1 - Tentar Conexão STM32", tag="API UI")
            ui.print_message("0 - Sair", tag="API UI")
            option = ui.prompt("Selecione uma opção: ", tag="API UI")
            if option == "1":
                comm = create_connection()
                if comm.is_connected:
                    comm.start_listening()
                    ui.print_status("Conexão serial estabelecida com sucesso.", success=True)
                    ui.print_message("Aguardando que o CLI da STM32 entre no modo interativo (pressione ESC no CLI da STM32)...", tag="API UI")
                    interactive_mode_event.clear()
                    interactive_mode_event.wait()
                    ui.print_status("Modo interativo ativado.", success=True)
                else:
                    ui.print_message("Tentativa de conexão falhou. Tente novamente.", tag="API UI")
            elif option == "0":
                ui.print_message("Saindo...", tag="API UI")
                break
            else:
                ui.print_message("Opção inválida. Tente novamente.", tag="API UI")
        else:
            option = ui.show_menu()  # Menu: "1 - Enviar RFID", "0 - Sair"
            if option == "1":
                ui.print_message("Enviando comando RFID...", tag="API UI")
                comm.send(RFIDCommand())
            elif option == "0":
                ui.print_message("Saindo do modo interativo...", tag="API UI")
                break
            else:
                ui.print_message("Opção inválida. Tente novamente.", tag="API UI")

    if comm.is_connected:
        comm.close()
        ui.print_status("Conexão serial fechada.", success=True)

if __name__ == "__main__":
    main()
