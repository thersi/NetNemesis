from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import serial
import time


class controller:
    def __init__(self, form):
        self.form = form
        ser = serial.Serial('COM3', 9600, timeout=1)

        form.onButton.clicked.connect(lambda: ser.write(str.encode(
            '<GUIREADY>')))
        form.offButton.clicked.connect(
            lambda: ser.write(str.encode('<NOTREADY>')))

# 'Servo1: 200; Servo2: 200; Servo3: 200; Servo4: 200; Servo5: 200; Servo6: 200;'
