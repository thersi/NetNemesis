import numpy as np
import time
import threading
import serial
import serial.tools.list_ports

class Driver:    
    def __init__(self, arm, xbxCtrl, dt, controller):
        self.arm = arm        
        self.xbxCtrl = xbxCtrl
        self.dt = dt/2 #update twice per computed control signal
        self.controller = controller
        ports = serial.tools.list_ports.comports()

        if (len(ports) == 0):
            print("No serial ports found")
            exit()

        for port in ports:
            if ("Arduino Uno" in port.description):
                print("Arduino Uno found on port: " + port.device)
                comport = port.device

        self.ser = serial.Serial(comport, 9600, timeout=0.5)

        x = threading.Thread(target=self._readData, daemon=True)
        x.start()

        y = threading.Thread(target=self._sendData, daemon=True)
        y.start()

        time.sleep(2)

    def _readData(self):
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline()
                if line:
                    string = line.decode()
                    if "<Ready>" in string:
                        print("Connection established")

                    if "<" in string and ">" in string and not "<Ready>" in string:
                        string = string.split(",")
                        ServoPos1 = int(string[0].translate({ord('<'): None}))
                        ServoPos2 = int(string[1])
                        ServoPos3 = int(string[2])
                        ServoPos4 = int(string[3])
                        ServoPos5 = int(string[4])
                        ServoPos6 = int(string[5].translate({ord('>'): None}))

                        print("<" + str(ServoPos1) + ", " + str(ServoPos2) + ", " + str(ServoPos3) +
                              ", " + str(ServoPos4) + ", " + str(ServoPos5) + ", " + str(ServoPos6) + ">")
                        self.arm.q[0] = ServoPos1*np.pi/180.0
                        self.arm.q[1] = ServoPos2*np.pi/180.0
                        self.arm.q[2] = ServoPos3*np.pi/180.0
                        self.arm.q[3] = ServoPos4*np.pi/180.0
                        self.arm.q[4] = ServoPos5*np.pi/180.0
                        self.arm.claw_angle = ServoPos6*np.pi/180.0

    def _sendData(self):
        while True:
            controller_state = self.xbxCtrl.read()
            claw = np.interp(controller_state[5], [0, 1], [10, 73])

            if self.controller.enabled: #use control signal in qd
                self.arm.qr = self.arm.q + self.dt*self.arm.qd #euler integrate next reference position for arm                
            
            servos = np.clip(self.arm.qr*180/np.pi, -135, 135)
            
            self.arm.q[4] = self.arm.qr[4] #encoder 4 does not work so we pretend it is perfect
            
            msg = "<" + ", ".join(str(int(s + 0.5)) for s in np.append(servos, claw)) + ">"
            self.ser.write(str.encode(msg))
            
            time.sleep(self.dt)