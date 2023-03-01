from numpy import angle
from genpy import struct_I
from init_robot import EiT_arm
import numpy as np


def main():
    """
    arm.q[0] = q1 (rotation about joint 1)
    arm.q[1] = q2 (rotation about joint 2)
    arm.q[2] = q3 (rotation about joint 3)
    arm.q[3] = q4 (rotation about joint 4)
    arm.q[4] = q5 (rotation of end effector)
    """

    print("Initialized digital twin: ")
    arm = EiT_arm()
    print(arm)
    print("Sets initial anglles to: [0,0,0,0,0]")
    arm.q = list([0,0,0,0,0])

    arm.plot(arm.q)
  
    print("\nInsert list of alngles: ")
    print("Example: 20 20 20 20 20")

    stringInput = input()
    print("Your input was: ")
    print(stringInput)
    anglelist = [float(s)*np.pi/180 for s in stringInput.split(' ')]
    arm.q = anglelist
    arm.plot(arm.q)

    print("Press a key to end.")
    input()


main()
