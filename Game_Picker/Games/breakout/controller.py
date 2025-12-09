import serial
import time

class Controller:
    ser = None
    buffer = None

    def connect(port):
        try:
            Controller.ser = serial.Serial(port, 9600)
            Controller.buffer = ""
            print(f"connected to {port}")
        except:
            print(f"could not connected to {port}")

    def readline():
        if Controller.ser is None:
            return None
        try:
            while Controller.ser.in_waiting > 0:
                ch = Controller.ser.read(1)
                ch = bytes.decode(ch)
                if ch == '\n':
                    line = Controller.buffer
                    Controller.buffer = ""
                    return(line)
                elif ch == '\r':
                    pass
                else:
                    Controller.buffer += ch
            return None
        except:
            print("disconnected")
            Controller.ser = None
        return None
    def readdata():
        line = Controller.readline()
        if line is None:
            return
        line = line.split()
        for i in range(1, len(line)):
            line[i] = int(line[i])
        return line
def main():
    Controller.connect("/dev/ttyUSB0")
    while 1:
        line = Controller.readdata()
        if line is not None:
            print (f"readdata {line}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
