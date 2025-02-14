import threading
import time
import usb.core
import usb.util
import serial
import serial.serialutil
import json

# ANSI color codes for terminal:
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

# List of authorized devices (VID/PID)
AUTHORIZED_DEVICES = [
    {"vid": 0x1a86, "pid": 0x55d4},   # Random example
    {"vid": 0x1a2c, "pid": 0x45ea},   # ESP32
    {"vid": 0x483,  "pid": 0x374e},   # ST-Link
]

# Serial port and baud rate settings:
CONNECTION_PORT = "COM6"
CONNECTION_BAUDRATE = 115200


def list_usb_devices():
    devices = usb.core.find(find_all=True)
    found_any = False
    for device in devices:
        found_any = True
        vid = hex(device.idVendor)
        pid = hex(device.idProduct)
        print(f"Device found: VID={vid}, PID={pid}")
    if not found_any:
        print("No USB devices found.")


def check_authorized_device():
    devices = usb.core.find(find_all=True)
    for dev in devices:
        vid = dev.idVendor
        pid = dev.idProduct
        for auth_dev in AUTHORIZED_DEVICES:
            if vid == auth_dev["vid"] and pid == auth_dev["pid"]:
                return True
    return False


class UIThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = False
        self._stop_event = threading.Event()

        # Track the connection status for Maestro (serial) and ITDM (socket):
        self.maestro_connected = False
        self.itdm_connected = False
        self.monitor_thread = None

    def run(self):
        self._print_status()

        while not self._stop_event.is_set():
            cmd = input("[UIThread] Enter a command (list/send/quit): ").strip().lower()

            if cmd == "list":
                list_usb_devices()
                self._print_status()

            elif cmd == "send":
                if self.monitor_thread:
                    self.monitor_thread.send_json_process()
                else:
                    print("[UIThread] No monitor thread available.")
                self._print_status()

            elif cmd == "quit":
                print("[UIThread] Exiting application...")
                if self.monitor_thread:
                    self.monitor_thread.stop()
                self._stop_event.set()

            else:
                print("Invalid command. Use: list, send, or quit.")
                self._print_status()

        print("[UIThread] UI thread stopped.")

    def OnMaestroConnectionUpdate(self, is_connected: bool):
        self.maestro_connected = is_connected
        status_str = "CONNECTED" if is_connected else "DISCONNECTED"
        print(f"[UIThread] Maestro is now {status_str}.")
        self._print_status()

    def OnITDMConnectionUpdate(self, is_connected: bool):
        self.itdm_connected = is_connected
        status_str = "CONNECTED" if is_connected else "DISCONNECTED"
        print(f"[UIThread] ITDM is now {status_str}.")
        self._print_status()

    def _print_status(self):
        if self.maestro_connected:
            maestro_status = f"{COLOR_GREEN}[Connected]{COLOR_RESET}"
        else:
            maestro_status = f"{COLOR_RED}[Disconnected]{COLOR_RESET}"

        if self.itdm_connected:
            itdm_status = f"{COLOR_GREEN}[Connected]{COLOR_RESET}"
        else:
            itdm_status = f"{COLOR_RED}[Disconnected]{COLOR_RESET}"

        print(
            f"Maestro {maestro_status} (Serial)  -  "
            f"ITDM {itdm_status} (Socket)"
        )

    def stop(self):
        self._stop_event.set()


class DeviceMonitorThread(threading.Thread):

    def __init__(self, ui_thread: UIThread, port=CONNECTION_PORT,
                 baudrate=CONNECTION_BAUDRATE, check_interval=1.0):
        super().__init__()
        self.daemon = True
        self.ui_thread = ui_thread
        self._stop_event = threading.Event()
        self.port = port
        self.baudrate = baudrate
        self.check_interval = check_interval
        self._serial = None

    def run(self):
        print("[DeviceMonitorThread] Starting continuous USB monitoring.")

        while not self._stop_event.is_set():
            device_present = check_authorized_device()

            if device_present and not self.is_port_open():
                self._open_serial_port()

            elif not device_present and self.is_port_open():
                print("[DeviceMonitorThread] Authorized device removed. Closing port.")
                self._close_serial_port()

            # Sleep for the specified interval before re-checking
            time.sleep(self.check_interval)

        # If we are asked to stop, ensure the port is closed before exiting
        self._close_serial_port()
        print("[DeviceMonitorThread] Stopped monitoring.")

    def send_json_process(self):
        if not self.is_port_open():
            print("[DeviceMonitorThread] Serial port is not open. Cannot send JSON.")
            return

        try:
            data = {"process": True}
            json_data = json.dumps(data)
            self._serial.write(json_data.encode("utf-8"))
            self._serial.flush()
            print(f"[DeviceMonitorThread] Sent JSON: {json_data}")

            # Wait briefly to see if there's a response
            time.sleep(1)
            if self._serial.in_waiting > 0:
                response = self._serial.readline().decode("utf-8", errors="ignore").strip()
                print(f"[DeviceMonitorThread] Received response: {response}")
            else:
                print("[DeviceMonitorThread] No response received.")
        except serial.SerialException as e:
            print(f"[DeviceMonitorThread] Error sending/receiving data: {e}")
            self._close_serial_port()

    def stop(self):
        self._stop_event.set()

    def is_port_open(self):
        return self._serial is not None and self._serial.is_open

    def _open_serial_port(self):
        try:
            print(f"[DeviceMonitorThread] Opening port {self.port} at {self.baudrate} baud...")
            self._serial = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"[DeviceMonitorThread] Successfully opened port {self.port}.")
            if self.ui_thread:
                self.ui_thread.OnMaestroConnectionUpdate(True)
        except serial.SerialException as e:
            print(f"[DeviceMonitorThread] Error opening port {self.port}: {e}")
            self._serial = None

    def _close_serial_port(self):
        if self._serial and self._serial.is_open:
            try:
                self._serial.close()
                print(f"[DeviceMonitorThread] Closed port {self.port}.")
            except Exception as e:
                print(f"[DeviceMonitorThread] Error closing port {self.port}: {e}")
            finally:
                self._serial = None
                # Notify UI that Maestro is disconnected
                if self.ui_thread:
                    self.ui_thread.OnMaestroConnectionUpdate(False)


def main():

    print(r"""


██╗████████╗██████╗ ███╗   ███╗    ███╗   ███╗ █████╗ ██████╗ ███████╗████████╗██████╗  ██████╗    █████╗ ██████╗██╗
██║╚══██╔══╝██╔══██╗████╗ ████║    ████╗ ████║██╔══██╗██╔═══  ██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗ ██╔══██╗██╔══██╗██║    
██║   ██║   ██║  ██║██╔████╔██║    ██╔████╔██║███████║███████║███████╗   ██║   ██████╔╝██║   ██║ ███████║██████╔╝██║
██║   ██║   ██╚══██║██║╚██╔╝██║    ██║╚██╔╝██║██╔══██║██╔══   ╚════██║   ██║   ██╔══██╗██║   ██║ ██╔══██║██╔═══╝ ██║
██║   ██║   ████╔══╝██║ ╚═╝ ██║    ██║ ╚═╝ ██║██║  ██║██████║ ███████║   ██║   ██║  ██║╚██████╔╝ ██║  ██║██║     ██║
╚═╝   ╚═╝   ╚═══╝   ╚═╝     ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═╝  ██║╚═╝     ╚═╝
                                                                                                      ╚═╝                      
      mmmm  mmmmmmmm        
    mmmm::  mmmmmmmmmm..    
  mmmmmm  ::mmmmmmmmmmmm    
  mmmmmm      mmmm      mm  
  mmmm    mm  mm    mm  mm  
mmmmmm  mm    mm  mm    mm  
  mmmm  mm  mm    mm  mmmm  
  mm    mm  mm  ++    mmmm  
  mmmmmmmmmmmm  mmmmmmmm    
    mmmmmmmm    mmmmmmmm    
      mmmmmm  mmmmmmmm      
              mmmm          
===========================================
    """)

    print("=== API Started ===")

    # create the UI thread first
    ui_thread = UIThread()


    monitor_thread = DeviceMonitorThread(ui_thread=ui_thread,
                                         port=CONNECTION_PORT,
                                         baudrate=CONNECTION_BAUDRATE,
                                         check_interval=1.0)

    # let the UI know which thread to use for 'send'
    ui_thread.monitor_thread = monitor_thread

    # init threads
    monitor_thread.start()
    ui_thread.start()
    ui_thread.join()

    # if UI finishes, ensure the monitor thread stops
    monitor_thread.stop()
    monitor_thread.join()

    print("=== Application Stopped ===")


if __name__ == "__main__":
    main()
