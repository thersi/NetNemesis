from arm_sim.init_robot import EiT_arm
from xbox_controller import XboxController
import threading
import serial
import serial.tools.list_ports
import time
import re
import numpy as np

# check Driver file. Renamed version of this (maybe old?), and cleaner


class Controller(XboxController):
    def __init__(self, form):

        self.arm = EiT_arm()
        self.form = form
        ports = serial.tools.list_ports.comports()

        print("init")

        if (len(ports) == 0):
            print("No serial ports found")
            exit()

        for port in ports:
            if ("Arduino Uno" in port.description):
                print("Arduino Uno found on port: " + port.device)
                comport = port.device

        self.ser = serial.Serial(comport, 9600, timeout=0.5)

        x = threading.Thread(target=self._readDataThread, daemon=True)
        x.start()

        y = threading.Thread(target=self._sendDataThread, daemon=True)
        y.start()

        super().__init__()
        time.sleep(2)

    def _readDataThread(self):
        claw_deg = 0
        ServoPos1 = 90
        ServoPos2 = 0
        ServoPos3 = 180
        ServoPos4 = 180
        ServoPos5 = 0
        ServoPos6 = 10
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline()
                if line:
                    # curr_degs = self.arm.q_degrees()
                    # claw_deg = self.arm.claw_deg()

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

                    # self.arm.q_degrees(curr_degs)
                    # self.arm.claw_deg(claw_deg)

    def _sendDataThread(self):

        prevServo1 = 0
        prevServo2 = 0
        prevServo3 = 0
        prevServo4 = 0
        prevServo5 = 0
        prevServo6 = 0

        servo1int = 90
        servo1 = "90"
        servo2int = 0
        servo2 = "0"
        servo3int = 180
        servo3 = "180"
        servo4int = 180
        servo4 = "180"
        servo5int = 0
        servo5 = "0"

        while True:
            q_degrees = np.rint(self.arm.q_degrees()).astype(int)
            claw_deg = np.rint(self.arm.claw_deg()).astype(int)

            controller_state = self.read()

            if controller_state[9] == 1:
                servo1int = 90
                servo1 = "90"
                servo2int = 0
                servo2 = "0"
                servo3int = 180
                servo3 = "180"
                servo4int = 180
                servo4 = "180"
                servo5int = 0
                servo5 = "0"

            # servo2 = str(q_degrees[1])
            # servo1 = str(90)
            if controller_state[11] == 1:
                servo1int += 1
                if servo1int > 180:
                    servo1int = 180
                servo1 = str(servo1int)
            elif controller_state[12] == 1:
                servo1int -= 1
                if servo1int < 0:
                    servo1int = 0
                servo1 = str(servo1int)

            # servo2 = str(45)
            joy2 = int(np.interp(controller_state[1], [-1, 1], [0, 100]))
            if joy2 >= 65:
                # print(joy2)
                servo2int += 0.5  # + controller_state[1] * 2
                if servo2int >= 180:
                    servo2int = 180
                servo2 = str(int(servo2int))
            elif joy2 <= 35:
                # print(joy2)
                servo2int -= 0.5  # - controller_state[1] * 2
                if servo2int <= 0:
                    servo2int = 0
                servo2 = str(int(servo2int))

            # servo3 = str(180)
            joy3 = int(np.interp(controller_state[0], [-1, 1], [0, 100]))
            if joy3 >= 65:
                # print(joy3)
                servo3int += 0.5  # + controller_state[0] * 2
                if servo3int >= 180:
                    servo3int = 180
                servo3 = str(int(servo3int))
            elif joy3 <= 35:
                # print(joy3)
                servo3int -= 0.5  # - controller_state[0] * 2
                if servo3int <= 0:
                    servo3int = 0
                servo3 = str(int(servo3int))

            # servo4 = str(180)
            joy4 = int(np.interp(controller_state[2], [-1, 1], [0, 100]))
            if joy4 >= 65:
                # print(joy4)
                servo4int += 0.5  # + controller_state[2] * 2
                if servo4int >= 180:
                    servo4int = 180
                servo4 = str(int(servo4int))
            elif joy4 <= 35:
                # print(joy4)
                servo4int -= 0.5  # - controller_state[2] * 2
                if servo4int <= 0:
                    servo4int = 0
                servo4 = str(int(servo4int))

            # servo5 = str(90)
            joy5 = int(np.interp(controller_state[3], [-1, 1], [0, 100]))
            if joy5 >= 65:
                # print(joy5)
                servo5int += 0.5  # + controller_state[3] * 2
                if servo5int >= 180:
                    servo5int = 180
                servo5 = str(int(servo5int))
            elif joy5 <= 35:
                # print(joy5)
                servo5int -= 0.5  # - controller_state[3] * 2
                if servo5int <= 0:
                    servo5int = 0
                servo5 = str(int(servo5int))

            servo6 = str(int(np.interp(controller_state[5], [0, 1], [10, 73])))

            if prevServo1 != servo1 or prevServo2 != servo2 or prevServo3 != servo3 or prevServo4 != servo4 or prevServo5 != servo5 or prevServo6 != servo6:
                # print(str.encode("<" + servo1 + ", " + servo2 + ", " + servo3 + ", " + servo4 + ", " + servo5 + ", " + servo6 + ">"))
                self.ser.write(str.encode("<" + servo1 + ", " + servo2 + ", " +
                               servo3 + ", " + servo4 + ", " + servo5 + ", " + servo6 + ">"))
                prevServo1 = servo1
                prevServo2 = servo2
                prevServo3 = servo3
                prevServo4 = servo4
                prevServo5 = servo5
                prevServo6 = servo6

                # b'<90,45,180,180,90,10>'
