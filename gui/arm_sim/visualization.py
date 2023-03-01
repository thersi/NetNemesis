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
    print("Sets initial angles to: [0,0,0,0,0]")
    
    initialPose = arm.fkine([0,0,0,0,0])

    print("\nInsert list of alngles: ")
    print("Example: 20 20 20 20 20")

    stringInput = input()
    print("Your input was: ")
    print(stringInput)

    inputAngleList = [float(s)*np.pi/180 for s in stringInput.split(' ')]

    secondPose = arm.fkine(inputAngleList)

    #Animating:
    qt = arm.jtraj(initialPose, secondPose, 50)
    arm.plot(qt.q, backend='pyplot', movie='panda1.gif')  

    print("Press a key to end.")
    input()

if __name__ == "__main__":
    main()