from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog

from arm_sim.robot import *
from xbox_controller import *
import threading
import serial
import serial.tools.list_ports
import time
import re

ports = serial.tools.list_ports.comports()
global ser
ServoPos1 = 0
ServoPos2 = 0
ServoPos3 = 0
ServoPos4 = 0
ServoPos5 = 0
ServoPos6 = 0



oldServo1 = ""
oldServo2 = ""
oldServo3 = ""
oldServo4 = ""
oldServo5 = ""
oldServo6 = ""



class Controller(XboxController):
    def __init__(self, form, XboxController):
        self.form = form

        if (len(ports) == 0):
            print("No serial ports found")
            exit()
        
        for port in ports:
            if ("Arduino Uno" in port.description):
                print("Arduino Uno found on port: " + port.device)
                comport = port.device

        ser = serial.Serial(comport, 9600, timeout=0.5)
        time.sleep(2)


        def serialThread():
            global ServoPos1
            global ServoPos2
            global ServoPos3
            global ServoPos4
            global ServoPos5
            global ServoPos6
            
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline()
                    if line:
                        string = line.decode()
                        if "<Ready>" in string:
                            print("Connection established")
                        if "ServoPos1" in string:
                            tempArray = re.findall(r'\d+', string)
                            ServoPos1 = int(tempArray[1])
                            print("ServoPos1:", ServoPos1)
                        if "ServoPos2" in string:
                            tempArray = re.findall(r'\d+', string)
                            ServoPos2 = int(tempArray[1])
                            print("ServoPos2:", ServoPos2)
                        if "ServoPos3" in string:
                            tempArray = re.findall(r'\d+', string)
                            ServoPos3 = int(tempArray[1])
                            print("ServoPos3:", ServoPos3)
                        if "ServoPos4" in string:
                            tempArray = re.findall(r'\d+', string)
                            ServoPos4 = int(tempArray[1])
                            print("ServoPos4:", ServoPos4)
                        if "ServoPos5" in string:
                            tempArray = re.findall(r'\d+', string)
                            ServoPos5 = int(tempArray[1])
                            print("ServoPos5:", ServoPos5)
                        if "ServoPos6" in string:
                            tempArray = re.findall(r'\d+', string)
                            ServoPos6 = int(tempArray[1])
                            print("ServoPos6:", ServoPos6)
                    

        def sendDataThread():
            global servo1, servo2, servo3, servo4, servo5, servo6
            global oldServo1, oldServo2, oldServo3, oldServo4, oldServo5, oldServo6


            joy = XboxController
            joy.__init__(self)


            while True:
                controller = joy.read(self)
                servo1 = str(q_degrees[0])
                servo2 = str(q_degrees[1])
                servo3 = str(q_degrees[2])
                servo4 = str(q_degrees[3])
                servo5 = str(q_degrees[4])
                servo6 = str(int(np.interp(controller[4],[0,1],[10,73])))

                if oldServo1 != servo1:
                    print(str.encode("<Servo1: " + servo1  + ";>"))
                    ser.write(str.encode("<Servo1: " + servo1  + ";>"))
                    oldServo1 = servo1
                if oldServo2 != servo2:
                    print(str.encode("<Servo2: " + servo2  + ";>"))
                    ser.write(str.encode("<Servo2: " + servo2  + ";>"))
                    oldServo2 = servo2
                if oldServo3 != servo3:
                    print(str.encode("<Servo3: " + servo3  + ";>"))
                    ser.write(str.encode("<Servo3: " + servo3  + ";>"))
                    oldServo3 = servo3
                if oldServo4 != servo4:
                    print(str.encode("<Servo4: " + servo4  + ";>"))
                    ser.write(str.encode("<Servo4: " + servo4  + ";>"))
                    oldServo4 = servo4
                if oldServo5 != servo5:
                    print(str.encode("<Servo5: " + servo5  + ";>"))
                    ser.write(str.encode("<Servo5: " + servo5  + ";>"))
                    oldServo5 = servo5
                if oldServo6 != servo6:
                    #print(str.encode("<Servo6: " + servo6  + ";>"))
                    print(str.encode("<Servo1: " + servo1  + "; " + 'Servo2: ' + servo2 + "; " + 'Servo3: ' + servo3 + "; " + 'Servo4: ' + servo4 + "; " + 'Servo5: ' + servo5 + "; " + 'Servo6: ' + servo6 + ";>"))
                    #ser.write(str.encode("<Servo6: " + servo6  + ";>"))
                    ser.write(str.encode("<Servo1: " + servo1  + "; " + 'Servo2: ' + servo2 + "; " + 'Servo3: ' + servo3 + "; " + 'Servo4: ' + servo4 + "; " + 'Servo5: ' + servo5 + "; " + 'Servo6: ' + servo6 + ";>"))
                    oldServo6 = servo6

                time.sleep(0.1)
                
                # if oldServo1 != servo1 or oldServo2 != servo2 or oldServo3 != servo3 or oldServo4 != servo4 or oldServo5 != servo5 or oldServo6 != servo6:

                #     print(str.encode("<Servo1: " + servo1  + "; " + 'Servo2: ' + servo2 + "; " + 'Servo3: ' + servo3 + "; " + 'Servo4: ' + servo4 + "; " + 'Servo5: ' + servo5 + "; " + 'Servo6: ' + servo6 + ";>"))
                #     #print(str.encode('Servo6: ' + servo6 + ";"))
                #     ser.write(str.encode("<Servo1: " + servo1  + "; " + 'Servo2: ' + servo2 + "; " + 'Servo3: ' + servo3 + "; " + 'Servo4: ' + servo4 + "; " + 'Servo5: ' + servo5 + "; " + 'Servo6: ' + servo6 + ";>"))
                #     #ser.write(str.encode('Servo6: ' + servo6 + ";"))
                #     #time.sleep(0.5)

                #     oldServo1 = servo1
                #     oldServo2 = servo2
                #     oldServo3 = servo3
                #     oldServo4 = servo4
                #     oldServo5 = servo5
                #     oldServo6 = servo6

        x = threading.Thread(target=serialThread, daemon=True)
        x.start()   

        y = threading.Thread(target=sendDataThread, daemon=True)
        y.start()  


        #print(joy.self.rt)
    

        #print(str.encode('Servo1: ' + servo1  + "; " + 'Servo2: ' + servo2 + "; " + 'Servo3: ' + servo3 + "; " + 'Servo4: ' + servo4 + "; " + 'Servo5: ' + servo5 + ";"))     

        #form.onButton.clicked.connect(lambda: ser.write(str.encode(
        #    'Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 0;')))

        form.onButton.clicked.connect(lambda: ser.write(str.encode('Servo1: ' + servo6  + "; " + 'Servo2: ' + servo2 + "; " + 'Servo3: ' + servo3 + "; " + 'Servo4: ' + servo4 + "; " + 'Servo5: ' + servo5 + "; " + 'Servo6: ' + servo6 + ";")))
        form.offButton.clicked.connect(lambda: ser.write(str.encode('Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 73;')))

# 'Servo1: 200; Servo2: 200; Servo3: 200; Servo4: 200; Servo5: 200; Servo6: 200;'
# Test 'Servo1: 90; Servo2: 60; Servo3: 90; Servo4: 90; Servo5: 45; Servo6: 73;'
