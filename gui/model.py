from arm_sim.end_pos import EndPosition
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
from arm_sim.controller import Controller
from xbox_controller import XboxController


Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()

form.setupUi(window)

# Create figure with subplots
figure = plt.figure()
form.simulationLayout.addWidget(figure.canvas)

arm = EiT_arm(q0=[0.21, -0.03, 0.35, -1.90, -0.04])  # initial pose
# controller time steps, how often new qd is calculated and plots updated
dt = 0.1

# xbxCtrl = XboxController()
# Driver(arm, XboxController) ##assign to variable to avoid garbage collection?

env = rtb.backends.PyPlot.PyPlot()
env.launch(name="EiT environment", fig=figure)  # lauches a second plot
env.add(arm)
plt.close()  # closes second plot

ep = EndPosition(arm.fkine(arm.q).A, env.ax)
ep.set_pos(arm.fkine([0.61, -0.03, 0.35, -1.90, -0.04]).A)

ctr = Controller(arm, ep.get_pos(), dt)
ctr.start()


def set_sliders():
    ang = arm.q_degrees().astype(int)
    form.q1_slider.setValue(ang[0])
    form.q2_slider.setValue(ang[1])
    form.q3_slider.setValue(ang[2])
    form.q4_slider.setValue(ang[3])
    form.q5_slider.setValue(ang[4])


def slider_change():
    arr = [form.q1_slider.value(),
           form.q2_slider.value(),
           form.q3_slider.value(),
           form.q4_slider.value(),
           form.q5_slider.value()]

    qs = np.asarray(arr)*np.pi/180

    form.q1.setText(str(arr[0]))
    form.q2.setText(str(arr[1]))
    form.q3.setText(str(arr[2]))
    form.q4.setText(str(arr[3]))
    form.q5.setText(str(arr[4]))
    arm.q = qs  # Shall not be done this way as this should only be changed by encoders. Send using Driver


def initialize_view():
    # Set up angle slider 1
    form.q1_slider.setMinimum(-135)
    form.q1_slider.setMaximum(135)
    form.q1_slider.valueChanged.connect(slider_change)

    # Set up angle slider 2
    form.q2_slider.setMinimum(-135)
    form.q2_slider.setMaximum(135)
    form.q2_slider.valueChanged.connect(slider_change)

    # Set up angle slider 3
    form.q3_slider.setMinimum(-135)
    form.q3_slider.setMaximum(135)
    form.q3_slider.valueChanged.connect(slider_change)

    # Set up angle slider 4
    form.q4_slider.setMinimum(-135)
    form.q4_slider.setMaximum(135)
    form.q4_slider.valueChanged.connect(slider_change)

    # Set up angle slider 5
    form.q5_slider.setMinimum(-135)
    form.q5_slider.setMaximum(135)
    form.q5_slider.valueChanged.connect(slider_change)

    set_sliders()
    # Add modes to mode_select
    form.mode_select.addItems(["Auto", "Position", "Optimization"])
    form.mode_select.setCurrentIndex(0)


initialize_view()


def changeTab(tabIndex):
    if tabIndex == 0:
        ctr.disable()
        ep.disable()
        set_sliders()
    elif tabIndex == 1:
        ep.set_pos(arm.fkine(arm.q).A)
        ctr.set_position(ep.get_pos())
        ep.enable()
        ctr.enable()


form.tabWidget.currentChanged.connect(changeTab)
form.mode_select.currentIndexChanged.connect(
    lambda: ctr.change_mode(form.mode_select.currentText()))

inc = 0.02  # increments for movement
inc_a = 5*np.pi/180  # angular increments

form.x_up.clicked.connect(lambda: ep.translate(inc, 0, 0))
form.y_up.clicked.connect(lambda: ep.translate(0, inc, 0))
form.z_up.clicked.connect(lambda: ep.translate(0, 0, inc))
form.x_cc.clicked.connect(lambda: ep.rotate(inc_a, 0, 0))
form.y_cc.clicked.connect(lambda: ep.rotate(0, inc_a, 0))
form.z_cc.clicked.connect(lambda: ep.rotate(0, 0, inc_a))
form.x_down.clicked.connect(lambda: ep.translate(-inc, 0, 0))
form.y_down.clicked.connect(lambda: ep.translate(0, -inc, 0))
form.z_down.clicked.connect(lambda: ep.translate(0, 0, -inc))
form.x_c.clicked.connect(lambda: ep.rotate(-inc_a, 0, 0))
form.y_c.clicked.connect(lambda: ep.rotate(0, -inc_a, 0))
form.z_c.clicked.connect(lambda: ep.rotate(0, 0, -inc_a))


form.set_goal.clicked.connect(lambda: ctr.set_position(ep.get_pos()))
form.follow.stateChanged.connect(
    lambda: form.set_goal.setEnabled(not form.follow.isChecked()))


def q_change():  # will be removed when arm encoders are up
    while True:
        # get encoder values. Here simulated by forward euler integration
        arm.q = np.clip(arm.q + dt*arm.qd, arm.q_lims[0, :], arm.q_lims[1, :])
        time.sleep(dt)


t = threading.Thread(target=q_change, daemon=True)
t.start()


def update():  # update plot periodically
    env.robots[0].draw()
    ep.draw()

    follow = form.follow.isChecked()
    if follow:
        ctr.set_position(ep.get_pos())


# Initialize QTimer
timer = QTimer()
timer.timeout.connect(update)
timer.start(int(dt*500))

window.show()
app.exec()
