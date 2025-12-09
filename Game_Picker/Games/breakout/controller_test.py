class Controller:
    ser = None
    buffer = None

    def connect(port):
        Controller.ser = f"connected to {port}"
        Controller.buffer = "empty"

    def readline():
        print(f"reading from {Controller.ser}")
        Controller.buffer += ", some data"
        print(f"buffer: {Controller.buffer}")

Controller.connect("bar")
Controller.readline()
