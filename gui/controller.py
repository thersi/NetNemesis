from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import serial
import time


class Controller:
    def __init__(self, form):
        self.form = form
        ser = serial.Serial('COM4', 9600, timeout=1)

        form.onButton.clicked.connect(lambda: ser.write(str.encode(
            'Servo1: 50; Servo2: 50; Servo3: 50; Servo4: 50; Servo5: 50; Servo6: 50;')))
        form.offButton.clicked.connect(
            lambda: ser.write(str.encode('Servo1: 20; Servo2: 20; Servo3: 20; Servo4: 20; Servo5: 20; Servo6: 20;')))

# 'Servo1: 200; Servo2: 200; Servo3: 200; Servo4: 200; Servo5: 200; Servo6: 200;'
