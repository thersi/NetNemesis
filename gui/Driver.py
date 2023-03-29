import numpy as np
import time
import threading
import re
import serial
import serial.tools.list_ports

class Driver:    
    def __init__(self, arm, xbxCtrl):
        self.arm = arm        
        self.xbxCtrl = xbxCtrl
        
        ports = serial.tools.list_ports.comports()

        if (len(ports) == 0):
            print("No serial ports found")
            exit()

        for port in ports:
            if ("Arduino Uno" in port.description):
                print("Arduino Uno found on port: " + port.device)
                comport = port.device

        self.ser = serial.Serial(comport, 9600, timeout=0.5)


        self.servos = np.zeros(shape=arm.n)

        x = threading.Thread(target=self._readData, daemon=True)
        x.start()

        y = threading.Thread(target=self._sendData, daemon=True)
        y.start()

        time.sleep(2) ##WHY?

    def _readData(self):
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline()
                if line:
                    string = line.decode()
                    if "<Ready>" in string:
                        print("Connection established")

                    if "ServoPos1" in string:
                        tempArray = re.findall(r'\d+', string)
                        ServoPos1 = float(tempArray[1])

                        self.arm.q[0] = ServoPos1*np.pi/180.0

                        print("ServoPos1:", ServoPos1)

                    if "ServoPos2" in string:
                        tempArray = re.findall(r'\d+', string)
                        ServoPos2 = float(tempArray[1])

                        self.arm.q[1] = ServoPos2*np.pi/180.0

                        print("ServoPos2:", ServoPos2)

                    if "ServoPos3" in string:
                        tempArray = re.findall(r'\d+', string)
                        ServoPos3 = float(tempArray[1])

                        self.arm.q[2] = ServoPos3*np.pi/180.0

                        print("ServoPos3:", ServoPos3)

                    if "ServoPos4" in string:
                        tempArray = re.findall(r'\d+', string)
                        ServoPos4 = float(tempArray[1])

                        self.arm.q[3] = ServoPos4*np.pi/180.0

                        print("ServoPos4:", ServoPos4)

                    if "ServoPos5" in string:
                        tempArray = re.findall(r'\d+', string)
                        ServoPos5 = float(tempArray[1])

                        self.arm.q[4] = ServoPos5*np.pi/180.0

                        print("ServoPos5:", ServoPos5)

                    if "ServoPos6" in string:
                        tempArray = re.findall(r'\d+', string)
                        ServoPos6 = float(tempArray[1])

                        self.arm.claw_angle = ServoPos6*np.pi/180.0

                        print("ServoPos6:", ServoPos6)

    def _sendData(self): #send arm.qd, not arm.q?
        while True:
            controller = self.xbxCtrl.read()
            servos = self.arm.q_degrees()
            claw = str(int(np.interp(controller[4], [0, 1], [10, 73]))) ##self.arm.claw_degrees()?

            self.ser.write(str.encode("<" + ", ".join(str(s) for s in np.r_[servos, claw]) + ">"))