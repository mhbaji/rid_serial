import serial
from PyQt5.QtCore import pyqtSignal, QThread

class Lib_Serial(QThread):
    signal_serial = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.port = ""
        self.baudrate = 0
        self.timeout = 0
        self.thread_active = False
        self._serial = None

    def set(self, _port, _baudrate, _timeout=1):
        self.port = _port
        self.baudrate = _baudrate
        self.timeout = _timeout

    def connect(self):
        self._serial = serial.Serial(self.port, self.baudrate, self.timeout)

    def run(self):
        self.thread_active = True
        while self.thread_active:
            if self._serial.in_waiting > 0:
                recv = self._serial.read(self._serial.in_waiting)
                self.signal_serial.emit(recv)

    def stop(self):
        self.thread_active = False
        # self.quit()
