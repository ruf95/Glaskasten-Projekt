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
        return True
    except:
        print(f"could not connect to {port}")
        return False

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
                Controller.buffer = ""
            elif ch == '\r':
                pass
            else:
                Controller.buffer += ch
    except:
        print("disconnected")
        Controller.ser = None
    return None
    

def readdata():
    s = readline()
    if s == None:
        return None
    l = s.split()
    for i in range(1, len(l)):
        l[i] = int(l[i])
    return l
    
def main():
    connect("/dev/ttyUSB0")
    while 1:
        list = readdata()
        if list is not None:
            print(f"readdata {list}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
