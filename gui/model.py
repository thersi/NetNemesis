from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from arm_sim.init_robot import EiT_arm
import numpy as np
import roboticstoolbox as rtb
import threading
import time

from arm_sim.position_controller import position_controller
from controller import Controller
from xbox_controller import XboxController

Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

# Create figure with subplots
figure = Figure()
ax1 = figure.add_subplot(111, projection="3d")
canvas = FigureCanvas(figure)

layout = form.simulationLayout
layout.addWidget(canvas)


arm = EiT_arm()


dt = 0.05

ctr = position_controller(arm)
ctr.set_pos(arm.fkine([1, 0, 1, 0, 1]).A)
ctr.start(dt)
# Change the robot configuration to a ready position
arm.q = [0.21, -0.03, 0.35, -1.90, -0.04]


env = rtb.backends.PyPlot.PyPlot()


def q_change():
    flag = False
    while True:
        # get encoder values. Here simulated perfectly (no noise)
        arm.q = arm.q + dt*(arm.qd)
        if ctr.arrived:
            if flag:
                ctr.set_pos(arm.fkine([1, 0, 1, 0, 1]).A)
            else:
                ctr.set_pos(arm.fkine([0.61, -0.03, 0.35, -1.90, -0.04]).A)
            flag = not flag
        time.sleep(dt)


t = threading.Thread(target=q_change, daemon=True)
t.start()


env.launch("environment")

env.ax = ax1
env.add(arm)


def update():
    env.step(dt)
    canvas.draw()


# Initialize QTimer
timer = QTimer()
timer.timeout.connect(update)
timer.start(1)

Controller(XboxController)
window.showMaximized()
app.exec()
