import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime

class SerialMonitor:
    def __init__(self):
        self.serial_connection = None
        self.is_connected = False
        self.read_thread = None
        self.stop_reading = False
        
    def list_ports(self):
        """List all available serial ports"""
        ports = serial.tools.list_ports.comports()
        print("\nAvailable Serial Ports:")
        print("-" * 40)
        for i, port in enumerate(ports):
            print(f"{i+1}. {port.device} - {port.description}")
        return ports
    
    def connect(self, port, baudrate=9600, timeout=1):
        """Connect to serial port"""
        try:
            self.serial_connection = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            self.is_connected = True
            print(f"\n✓ Connected to {port} at {baudrate} baud")
            print("=" * 50)
            
            # Start reading thread
            self.stop_reading = False
            self.read_thread = threading.Thread(target=self._read_serial, daemon=True)
            self.read_thread.start()
            
            return True
            
        except serial.SerialException as e:
            print(f"✗ Failed to connect: {e}")
            return False
    
    def _read_serial(self):
        """Read data from serial port in separate thread"""
        while self.is_connected and not self.stop_reading:
            try:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    if data:
                        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                        print(f"[{timestamp}] {data}")
                time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                print(f"Read error: {e}")
                break
    
    def send_data(self, data):
        """Send data to serial port"""
        if self.is_connected and self.serial_connection:
            try:
                self.serial_connection.write((data + '\n').encode('utf-8'))
                print(f"Sent: {data}")
            except Exception as e:
                print(f"Send error: {e}")
        else:
            print("Not connected to any port!")
    
    def disconnect(self):
        """Disconnect from serial port"""
        if self.is_connected:
            self.stop_reading = True
            self.is_connected = False
            if self.serial_connection:
                self.serial_connection.close()
            print("\n✓ Disconnected")

def main():
    monitor = SerialMonitor()
    
    print("=" * 50)
    print("         PYTHON SERIAL MONITOR")
    print("=" * 50)
    
    while True:
        if not monitor.is_connected:
            # Show available ports
            ports = monitor.list_ports()
            
            if not ports:
                print("No serial ports found!")
                input("Press Enter to refresh...")
                continue
            
            # Get user input for port selection
            try:
                choice = input(f"\nSelect port (1-{len(ports)}) or 'q' to quit: ")
                if choice.lower() == 'q':
                    break
                
                port_index = int(choice) - 1
                if 0 <= port_index < len(ports):
                    selected_port = ports[port_index].device
                    
                    # Get baud rate
                    baud_input = input("Enter baud rate (default: 9600): ")
                    baudrate = int(baud_input) if baud_input else 9600
                    
                    # Connect
                    monitor.connect(selected_port, baudrate)
                    
                else:
                    print("Invalid selection!")
                    
            except ValueError:
                print("Invalid input!")
                continue
        
        else:
            # Connected - show options
            print("\nCommands:")
            print("  Type message and press Enter to send")
            print("  'disconnect' - Disconnect from port")
            print("  'clear' - Clear screen")
            print("  'quit' - Exit program")
            print("-" * 30)
            
            try:
                user_input = input()
                
                if user_input.lower() == 'disconnect':
                    monitor.disconnect()
                elif user_input.lower() == 'clear':
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif user_input.lower() == 'quit':
                    break
                else:
                    monitor.send_data(user_input)
                    
            except KeyboardInterrupt:
                print("\n\nCtrl+C pressed. Disconnecting...")
                monitor.disconnect()
                break
    
    # Cleanup
    monitor.disconnect()
    print("Goodbye!")

if __name__ == "__main__":
    # Install required package if not present
    try:
        import serial
    except ImportError:
        print("pyserial not installed. Install with: pip install pyserial")
        exit(1)
    
    main()