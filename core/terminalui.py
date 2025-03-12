class TerminalUI:
    def print_message(self, message, tag="API UI"):
        print(f"[{tag}]: {message}")

    def print_status(self, message, success=True):
        if success:
            # Verde para status estabelecido
            print(f"\033[92m[STATUS]: {message}\033[0m")
        else:
            # Vermelho para status não estabelecido
            print(f"\033[91m[STATUS]: {message}\033[0m")

    def prompt(self, message, tag="API UI"):
        return input(f"[{tag}]: {message}")

    def show_menu(self):
        self.print_message("Menu:", tag="API UI")
        self.print_message("1 - Enviar RFID", tag="API UI")
        self.print_message("0 - Sair", tag="API UI")
        return self.prompt("Selecione uma opção: ", tag="API UI")
