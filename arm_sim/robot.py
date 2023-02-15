import numpy as np
import roboticstoolbox.robot as robot
from inverse_kinematics import inverse_kinematics


links = [robot.RevoluteDH(d = 0.2, a = 0, alpha=np.pi/2),
         robot.RevoluteDH(d = 0, a = 1/2, alpha= 0),
         robot.RevoluteDH(d = 0, a = 1/2, alpha = -np.pi/2),
         robot.RevoluteDH(d = 0 , a = 0, alpha= -np.pi/2, offset= -np.pi/2),
         robot.RevoluteDH(d = 1/8 , a = 0, alpha=0)]


arm_manipulator = robot.DHRobot(links=links, name='EiT arm')

q = np.random.random(size=5)*np.pi - np.pi/2
print('angles ground truth:', q)

##analytical solution
arm_manipulator.q = q
Te = arm_manipulator.fkine(arm_manipulator.q)
inv = inverse_kinematics(Te, arm_manipulator)
print('angles analytically:', inv)

stack = np.vstack((q, inv))
pattern = np.tile(stack, (5, 1))

arm_manipulator.plot(pattern, dt=1) #simulate the two different solutions

##numerical solution
sol, success, iter, searches, res = arm_manipulator.ikine_LM(Te)

if not success:
    print('could not find inverse solution numerically')
else:
    print('angles numerically:', sol)
    arm_manipulator.plot(sol)
    input('press any key to close')