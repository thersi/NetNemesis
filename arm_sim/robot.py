import numpy as np
import roboticstoolbox as rtb
import roboticstoolbox.robot as robot
from spatialmath import SE3


links = [robot.RevoluteDH(d = 0.2, a = 0, alpha=np.pi/2),
         robot.RevoluteDH(d = 0, a = 1/2, alpha= 0),
         robot.RevoluteDH(d = 0, a = 1/2, alpha = -np.pi/2),
         robot.RevoluteDH(d = 0 , a = 0, alpha= -np.pi/2, offset= -np.pi/2),
         robot.RevoluteDH(d = 1/8 , a = 0, alpha=0)]


# links = [robot.RevoluteDH(d = 0.2, a = 0, alpha=np.pi/2),
#          robot.RevoluteDH(d = 0, a = 1/2, alpha= 0),
#          robot.RevoluteDH(d = 0, a = 0, alpha = -np.pi/2, offset=-np.pi/2),
#          robot.RevoluteDH(d = 1/2, a = 0, alpha = -np.pi/2, offset=np.pi/2),
#          robot.RevoluteDH(d = 0 , a = 0, alpha= np.pi/2, offset= -np.pi/2),
#          robot.RevoluteDH(d = 1/8 , a = 0, alpha=0)]


arm_manipulator = robot.DHRobot(links=links, name='EiT arm')
print(arm_manipulator)
print(arm_manipulator.isspherical())

arm_manipulator.plot([0,0,1,0,0])
input('press any key to close')

Te = arm_manipulator.fkine([1, 1.2, -1.1, 0.3, 0.3])

T = SE3.Trans(0.6, -0.3, 0.1)*SE3.OA([0, 1, 0], [0, 0, -1])
# sol, success, iter, searches, res = arm_manipulator.ik_lm_chan(T)
sol, success, iter, searches, res = arm_manipulator.ik_lm_chan(Te)

if not success:
    print('could not find inverse solution')
else:
    arm_manipulator.plot(sol)
    input('press any key to close')
