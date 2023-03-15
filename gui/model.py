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


def q_change():
    while True:
        arm.q += 0.3*np.random.random(size=arm.q.shape)
        time.sleep(dt)


t = threading.Thread(target=q_change, daemon=True)
t.start()


env = rtb.backends.PyPlot.PyPlot()

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


# Controller(form)
window.showMaximized()
app.exec()
