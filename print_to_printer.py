from serial import Serial
import time

def print_to_printer(text, port='/dev/cu.usbserial-110', baudrate=9600):
    try:
        # Open serial connection to Arduino
        print(f"Attempting to connect to {port}...")
        ser = Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for Arduino to initialize
        
        # Send the text
        print(f"Sending text: {text}")
        ser.write(f"{text}\n".encode())
        
        # Close the connection
        ser.close()
        print("Print successful!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure:")
        print("1. The Arduino is connected")
        print("2. The correct port is specified")
        print("3. No other program is using the serial port")
        return False

# Example usage:
if __name__ == "__main__":
    # Replace with your actual text or function output
    text_to_print = "Hello from Python!"
    
    # Print the text
    print_to_printer(text_to_print) 