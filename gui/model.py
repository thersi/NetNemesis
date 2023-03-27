from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
import threading
import time
import numpy as np

from arm_sim.init_robot import EiT_arm
from Driver import Driver
from xbox_controller import XboxController


from arm_sim.controller import Controller
from arm_sim.end_pos_controller import EndPosition


Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

# Create figure with subplots
figure = plt.figure()
form.simulationLayout.addWidget(figure.canvas)

arm = EiT_arm(q0 = [0.21, -0.03, 0.35, -1.90, -0.04]) #initial pose
#controller time steps, how often new qd is calculated and plots updated
dt = 0.1


env = rtb.backends.PyPlot.PyPlot()
env.launch(name = "EiT environment", fig=figure) #lauches a second plot
env.add(arm)
plt.close() #closes second plot

ep = EndPosition(arm.fkine(arm.q).A, env.ax)
ep.set_pos(arm.fkine([0.61, -0.03, 0.35, -1.90, -0.04]).A)

ctr = Controller(arm, ep.get_pos(), dt)
ctr.start()

def q_change(): #will be removed when arm encoders are up
    while True:
        # get encoder values. Here simulated by forward euler integration
        arm.q = np.clip(arm.q + dt*arm.qd, arm.q_lims[0, :], arm.q_lims[1, :])
        time.sleep(dt)

t = threading.Thread(target=q_change, daemon=True)
t.start()

def change_ep(): #simulate user input to change end effector position
    T_new = arm.fkine(np.random.random(size=5)*1.5*np.pi-0.75*np.pi).A
    while T_new[2, 3] <= 0: #need positive z-position (above ground)
        T_new = arm.fkine(np.random.random(size=5)*1.5*np.pi-0.75*np.pi).A

    ep.set_pos(T_new)
    ctr.set_position(ep.get_pos())


def update(): #update plot periodically
    env.robots[0].draw()
    ep.draw()


# Initialize QTimer
timer = QTimer()
timer.timeout.connect(update)
timer.start(int(dt*1000))

form.onButton.clicked.connect(change_ep)

modes = ["Auto", "Position", "Optimization"]
i = 0
def nextMode():
    global i
    m = modes[i]
    i = (i+1)%3
    return m
form.offButton.clicked.connect(lambda : ctr.change_mode(nextMode()))

# xbxCtrl = XboxController()
# Driver(arm, XboxController) ##assign to variable to avoid garbage collection?
window.showMaximized()
app.exec()
