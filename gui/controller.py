from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import serial
import time


class Controller:
    def __init__(self, form):
        self.form = form
        ser = serial.Serial('COM4', 9600, timeout=1)

        form.onButton.clicked.connect(lambda: ser.write(str.encode(
            'Servo1: 80; Servo2: 80; Servo3: 80; Servo4: 80; Servo5: 80; Servo6: 80;')))
        form.offButton.clicked.connect(
            lambda: ser.write(str.encode('Servo1: 0; Servo2: 0; Servo3: 0; Servo4: 0; Servo5: 0; Servo6: 0;')))

# 'Servo1: 200; Servo2: 200; Servo3: 200; Servo4: 200; Servo5: 200; Servo6: 200;'
