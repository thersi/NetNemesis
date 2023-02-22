from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog

from arm_sim.robot import *

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
        servo1 = q_degrees[0]
        servo1 = str(servo1)
        servo2 = q_degrees[1]
        servo2 = str(servo2)
        servo3 = q_degrees[2]
        servo3 = str(servo3)
        servo4 = q_degrees[3]
        servo4 = str(servo4)
        servo5 = q_degrees[4]
        servo5 = str(servo5)
    

        #print(str.encode('Servo1: ' + servo1  + "; " + 'Servo2: ' + servo2 + "; " + 'Servo3: ' + servo3 + "; " + 'Servo4: ' + servo4 + "; " + 'Servo5: ' + servo5 + ";"))     

        #form.onButton.clicked.connect(lambda: ser.write(str.encode(
        #    'Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 0;')))

        form.onButton.clicked.connect(lambda: ser.write(str.encode('Servo1: ' + servo1  + "; " + 'Servo2: ' + servo2 + "; " + 'Servo3: ' + servo3 + "; " + 'Servo4: ' + servo4 + "; " + 'Servo5: ' + servo5 + ";")))
        form.offButton.clicked.connect(
            lambda: ser.write(str.encode('Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 73;')))

# 'Servo1: 200; Servo2: 200; Servo3: 200; Servo4: 200; Servo5: 200; Servo6: 200;'
# Test 'Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 73;'
