class TerminalUI:
    def print_message(self, message, tag="API UI"):
        print(f"[{tag}]: {message}")

    def print_status(self, message, success=True):
        if success:
            print(f"\033[92m[STATUS]: {message}\033[0m")  # Green
        else:
            print(f"\033[91m[STATUS]: {message}\033[0m")  # Red

    def prompt(self, message, tag="API UI"):
        return input(f"[{tag}]: {message}")

    def show_menu(self):
        self.print_message("Menu:", tag="API UI")
        self.print_message("1 - Send RFID Command", tag="API UI")
        self.print_message("0 - Exit", tag="API UI")
        return self.prompt("Select an option: ", tag="API UI")
