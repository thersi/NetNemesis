
import numpy as np

import roboticstoolbox as rtb
import threading
import time

from arm_sim.init_robot import EiT_arm


arm = EiT_arm()


dt = 0.05


def q_change():
    while True:
        arm.q += 0.3*np.random.random(size=arm.q.shape)
        time.sleep(dt)


t = threading.Thread(target=q_change, daemon=True)
t.start()


env = rtb.backends.PyPlot.PyPlot()

env.launch("environment")
env.add(arm)


while True:
    env.step(dt)