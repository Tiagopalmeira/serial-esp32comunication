import threading
import time
import queue
from core.terminalui import TerminalUI
from core.communication import Communication
from commands.rfid_command import RFIDWrite
from commands.fingerprint_count import FPCount
from commands.fingerprint_enroll import FPUnenroll
from commands.fingerprint_enroll import FPEnrollSubscribe
from commands.fingerprint_enroll import FPEnrollBegin
from commands.fingerprint_enroll import FPEnrollCapture
from commands.fingerprint_enroll import FPEnrollFinalize

def user_input_loop(ui, input_queue):
    while True:
        user_in = ui.prompt("", tag="API UI")
        input_queue.put(user_in)
        if user_in.strip() == "0":
            break

def print_disconnected_menu(ui):
    ui.print_status("Error: Serial connection not established.", success=False)
    ui.print_message("1 - Attempt to Connect to STM32", tag="API UI")
    ui.print_message("0 - Exit", tag="API UI")

def print_connected_menu(ui):
    ui.print_message("Menu:", tag="API UI")
    ui.print_message("1 - Send FP Unrenroll", tag="API UI")
    ui.print_message("2 - Send FP Subscribe", tag="API UI")
    ui.print_message("3 - Send FP Begin", tag="API UI")
    ui.print_message("4 - Send FP Capture", tag="API UI")
    ui.print_message("5 - Send FP Finalize", tag="API UI")

    ui.print_message("0 - Exit", tag="API UI")

def main():
    ui = TerminalUI()
    interactive_mode_event = threading.Event()
    input_queue = queue.Queue()
    should_print_menu = True

    def stm32_callback(message):
        ui.print_message(message, tag="STM32")
        
        # Se houver texto indicando que devemos enviar ESC
        if "press esc to" in message.lower() and "interactive mode" in message.lower():
            ui.print_message("Sending ESC to STM32...", tag="API UI")
            if comm.ser:
                comm.ser.write(b"\x1B")

        # Se o firmware indicar que está "now in interactive mode"
        if "now" in message.lower() and "interactive mode" in message.lower():
            interactive_mode_event.set()

    def create_connection():
        return Communication(port="COM7", baud_rate=115200, callback=stm32_callback)

    comm = create_connection()
    if comm.is_connected:
        comm.start_listening()
        ui.print_status("Serial connection established successfully.", success=True)
        ui.print_message("Waiting for the STM32 messages...", tag="API UI")
        interactive_mode_event.wait()
        ui.print_status("Interactive mode activated.", success=True)
    else:
        ui.print_status("Error: Serial connection not established.", success=False)

    # Thread dedicada para input do usuário
    input_thread = threading.Thread(target=user_input_loop, args=(ui, input_queue), daemon=True)
    input_thread.start()

    while True:
        if not comm.is_connected:
            if should_print_menu:
                print_disconnected_menu(ui)
                should_print_menu = False

            try:
                option = input_queue.get(timeout=0.2)
            except queue.Empty:
                option = None

            if option:
                if option.strip() == "1":
                    comm = create_connection()
                    if comm.is_connected:
                        comm.start_listening()
                        ui.print_status("Serial connection established successfully.", success=True)
                        interactive_mode_event.clear()
                        interactive_mode_event.wait()
                        ui.print_status("Interactive mode activated.", success=True)
                    else:
                        ui.print_message("Connection attempt failed. Please try again.", tag="API UI")
                    should_print_menu = True
                elif option.strip() == "0":
                    ui.print_message("Exiting...", tag="API UI")
                    break
                else:
                    #ui.print_message("Invalid option. Please try again.", tag="API UI")
                    should_print_menu = True

        else:
            if should_print_menu:
                print_connected_menu(ui)
                should_print_menu = False

            try:
                option = input_queue.get(timeout=0.2)
            except queue.Empty:
                option = None

            if option:
                if option.strip() == "1":
                    comm.send(FPUnenroll())
                    should_print_menu = True
                if option.strip() == "2":
                    comm.send(FPEnrollSubscribe())
                    should_print_menu = False
                if option.strip() == "3":
                    comm.send(FPEnrollBegin())
                    should_print_menu = False
                if option.strip() == "4":
                    comm.send(FPEnrollCapture())
                    should_print_menu = False
                if option.strip() == "5":
                    comm.send(FPEnrollFinalize())
                    should_print_menu = False
                elif option.strip() == "0":
                    ui.print_message("Exiting interactive mode...", tag="API UI")
                    break

        time.sleep(0.1)

    if comm.is_connected:
        comm.close()
        ui.print_status("Serial connection closed.", success=True)

    input_thread.join(timeout=1)

if __name__ == "__main__":
    main()
