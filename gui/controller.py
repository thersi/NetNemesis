from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import serial
import time


class Controller:
    def __init__(self, form):
        self.form = form
        ser = serial.Serial('COM4', 9600, timeout=1)

        form.onButton.clicked.connect(lambda: ser.write(str.encode(
            'Servo1: 90; Servo2: 45; Servo3: 180; Servo4: 180; Servo5: 0; Servo6: 30;')))
        form.offButton.clicked.connect(
            lambda: ser.write(str.encode('Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 73;')))

# 'Servo1: 200; Servo2: 200; Servo3: 200; Servo4: 200; Servo5: 200; Servo6: 200;'
