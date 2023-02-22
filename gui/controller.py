from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import serial
import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()

class Controller:
    def __init__(self, form):
        self.form = form

        if (len(ports) == 0):
            print("No serial ports found")
            exit()
        
        for port in ports:
            if ("Arduino Uno" in port.description):
                print("Arduino Uno found")
                comport = port.device

        

        
        ser = serial.Serial(comport, 9600, timeout=1)
        time.sleep(2)
        
        line = ser.readline()
        if line:
            string = line.decode()
            if "<Ready>" in string:
                print(string)
                

        form.onButton.clicked.connect(lambda: ser.write(str.encode(
            'Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 10;')))
        form.offButton.clicked.connect(
            lambda: ser.write(str.encode('Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 73;')))

# 'Servo1: 200; Servo2: 200; Servo3: 200; Servo4: 200; Servo5: 200; Servo6: 200;'
# Test 'Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 73;'
