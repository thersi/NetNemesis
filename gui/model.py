from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
import threading
import time

from arm_sim.init_robot import EiT_arm
from arm_sim.position_controller import position_controller
from arm_sim.optimization_controller import optimization_controller
from Driver import Driver
from xbox_controller import XboxController

Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

# Create figure with subplots
figure = plt.figure()
form.simulationLayout.addWidget(figure.canvas)

arm = EiT_arm(q0 = [0.21, -0.03, 0.35, -1.90, -0.04]) #initial pose

#controller time steps, how often new qd is calculated
dt = 0.1

# ctr = position_controller(arm)
ctr = optimization_controller(arm)

ctr.set_pos(arm.fkine([1, 0, 1, 0, 1]).A)
ctr.start(dt)

env = rtb.backends.PyPlot.PyPlot()
env.launch(name = "environment", fig=figure) #lauches a second plot. could copy robotic toolbox source and comment out plt.show() insted. should solve issue
env.add(arm)

def q_change(): #will be romved when arm encoders are up
    flag = False
    while True:
        # get encoder values. Here simulated perfectly (no noise)
        arm.q = arm.q + dt*arm.qd
        if ctr.arrived:
            if flag:
                ctr.set_pos(arm.fkine([1, 0, 1, 0, 1]).A)
            else:
                ctr.set_pos(arm.fkine([0.61, -0.03, 0.35, -1.90, -0.04]).A)
            flag = not flag
        time.sleep(dt)

t = threading.Thread(target=q_change, daemon=True)
t.start()

def update(): #update plot periodically
    # env.step(dt) #this lauches the second plot on every iteration

    env.robots[0].draw() #easy hack by inspection of toolbox source code, perhaps should redraw something more later
    #consequence is that time is not shown, however not important for our use (I think)

    # figure.canvas.draw() #for some reason not neccessary


# Initialize QTimer
timer = QTimer()
timer.timeout.connect(update)
timer.start(dt)

# xbxCtrl = XboxController()
# Driver(arm, XboxController) ##assign to variable to avoid garbage collection?
window.showMaximized()
app.exec()
