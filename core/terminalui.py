class TerminalUI:
    def print_message(self, message, tag="API UI"):
        print(f"[{tag}]: {message}")

    def print_status(self, message, success=True):
        if success:
            print(f"\033[92m[STATUS]: {message}\033[0m")
        else:
            print(f"\033[91m[STATUS]: {message}\033[0m")

    def prompt(self, message, tag="API UI"):
        return input(f"")
