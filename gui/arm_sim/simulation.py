import numpy as np
import roboticstoolbox as rt

from init_robot import EiT_arm
from position_controller import arm_controller

import time


arm = EiT_arm([0, 0, 0, 0, 0])

ctr = arm_controller(arm)
ctr.set_pos(arm.fkine([1, 1, -1, 1, 1]).A)

dt = 0.01

qs = []

kt = 1.0
kr = 1.3
k = np.array([kt, kt, kt, kr, kr, kr])

done = False

while not done:
    arm.qd, done = ctr.control_loop(k)
    arm.q = arm.q + arm.qd*dt #euler integrate    
    qs.append(arm.q)

    # time.sleep(dt)


print(np.array(qs).shape)
arm.plot(np.array(qs)[::5,:], dt=0.01, loop=True)

input("press any key to quit")
exit(1)