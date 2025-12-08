import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)

print("Warten auf serielle Eingabe...")

while True:
    buffer = ""
    while ser.in_waiting > 0:
        ch = ser.read(1)
        ch = ch.decode()
        if ch == '\n':
            print(f"Zeile> {buffer}")
            buffer = ""
        elif ch == '\r':
            pass
        else:
            buffer += ch
    time.sleep(0.1)
    
