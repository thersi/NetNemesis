from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

import matplotlib.pyplot as plt
import roboticstoolbox as rtb
import threading
import time
import numpy as np

from arm_sim.end_pos import EndPosition
from arm_sim.init_robot import EiT_arm
from arm_sim.controller import Controller

from Driver import Driver
from xbox_controller import XboxController

##PROGRAM FLAGS
SIMULATE = False #if true then no interfacing with hardware, and motion is simulated
USE_XBX_CTR = True

##SIM PARMS
dt = 0.1 # controller time steps, how often new qd is calculated
update_dt = dt/4 # how often plots are updated

##INIT ARM MODEL
arm = EiT_arm(q0=[0.21, -0.03, 0.35, -1.90, -0.04])  # initial pose

##INIT GUI
Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

figure = plt.figure() # Create figure with subplots
form.simulationLayout.addWidget(figure.canvas)

env = rtb.backends.PyPlot.PyPlot()
env.launch(name="EiT environment", fig=figure)  # lauches a second plot
env.add(arm)
plt.close()  # closes second plot

## CONTROL
ep = EndPosition(arm.fkine(arm.q).A, env.ax, reach=arm.length) #the end position axes in the plot
ctr = Controller(arm, ep.get_pos(), dt) #arm controller when in end-position mode
ctr.start()

## XBOX
if USE_XBX_CTR or not SIMULATE: #need xbox controller if hardware is used to control claw
    xbxCtrl = XboxController()

## HARDWARE
if not SIMULATE:
    driver = Driver(arm, xbxCtrl, dt, ctr) ##assign to variable to avoid garbage collection?

##GUI setup
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

    form.q1.setText(str(arr[0]))
    form.q2.setText(str(arr[1]))
    form.q3.setText(str(arr[2]))
    form.q4.setText(str(arr[3]))
    form.q5.setText(str(arr[4]))

    qs = np.asarray(arr)*np.pi/180
    arm.qr = qs  #Sets reference q

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

inc = 0.02  # increments for movement on button press
inc_a = 5*np.pi/180  # angular increments
inc_analog = 0.01 #increments for joystick

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

def inc_arm_ref(i, x):
    if abs(x) < 0.15:
        return
    
    sliders = [form.q1_slider, form.q2_slider, form.q3_slider, form.q4_slider, form.q5_slider]
    labels = [form.q1, form.q2, form.q3, form.q4, form.q5]


    new_qr = arm.qr[i] + inc_analog*x
    q_deg = (new_qr*180/np.pi + 0.5).astype(int)

    
    if abs(q_deg) < 135:
        arm.qr[i] = new_qr 
        sliders[i].setSliderPosition(q_deg)
        labels[i].setText(str(q_deg))

def register_xbx_funcs(mode):
    for code in ['ABS_X', 'ABS_Y', 'ABS_RX', 'ABS_RY', 'BTN_TR', 'BTN_TL', 'BTN_NORTH', 'BTN_SOUTH', 'BTN_WEST', 'BTN_EAST']:
        xbxCtrl.unregister_event_function(code)

    if mode == 0:
        xbxCtrl.register_event_function('BTN_TL', lambda _: inc_arm_ref(0, 3)) #bumper behind, 3 to give greater effect
        xbxCtrl.register_event_function('BTN_TR', lambda _: inc_arm_ref(0, -3)) #bumper behind
        xbxCtrl.register_event_function('ABS_Y', lambda x: inc_arm_ref(1, x)) #left joystick up/down
        xbxCtrl.register_event_function('ABS_X', lambda x: inc_arm_ref(2, x)) #left joystick left/right
        xbxCtrl.register_event_function('ABS_RY', lambda x: inc_arm_ref(3, x)) #right joystick up/down
        xbxCtrl.register_event_function('ABS_RX', lambda x: inc_arm_ref(4, x)) #right joystick left/right

    elif mode == 1: #follow end position
        xbxCtrl.register_event_function('ABS_Y', lambda x: ep.translate(inc_analog*x, 0, 0)) #left joystick up/down
        xbxCtrl.register_event_function('ABS_X', lambda x: ep.translate(0, inc_analog*x, 0)) #left joystick left/right
        xbxCtrl.register_event_function('ABS_RY', lambda x: ep.translate(0, 0, inc_analog*x)) #right joystick up/down

        xbxCtrl.register_event_function('BTN_WEST', lambda _: ep.rotate(inc_a, 0, 0)) #X-button, rotate X ccw
        xbxCtrl.register_event_function('BTN_NORTH', lambda _: ep.rotate(0, inc_a, 0)) #Y-Button, rotate Y ccw
        xbxCtrl.register_event_function('BTN_TR', lambda _: ep.rotate(0, 0, inc_a))  #right bumper, rotate Z ccw

        xbxCtrl.register_event_function('BTN_SOUTH', lambda _: ep.rotate(-inc_a, 0, 0)) #A-button, rotate X cw
        xbxCtrl.register_event_function('BTN_EAST', lambda _: ep.rotate(0, -inc_a, 0)) #B-Button, rotate Y cw
        xbxCtrl.register_event_function('BTN_TL', lambda _: ep.rotate(0, 0, -inc_a))  #left bumper, rotate Z cw
    else:
        raise ValueError(f"Invalid mode encountered in register_xbx_funcs. MODE: {mode}")
        
def changeTab(tabIndex):
    if USE_XBX_CTR:
        register_xbx_funcs(tabIndex) #change what xbox controller does

    if tabIndex == 0:
        ctr.disable()
        ep.disable()
        set_sliders()
    elif tabIndex == 1:
        ep.set_pos(arm.fkine(arm.q).A)
        ctr.set_position(ep.get_pos())
        ep.enable()
        ctr.enable()


form.tabWidget.currentChanged.connect(changeTab) #tabs
form.mode_select.currentIndexChanged.connect(lambda: ctr.change_mode(form.mode_select.currentText())) #rullgardin

form.set_goal.clicked.connect(lambda: ctr.set_position(ep.get_pos())) #set-goal button
form.follow.stateChanged.connect(lambda: form.set_goal.setEnabled(not form.follow.isChecked())) #enable/disable button on check

if USE_XBX_CTR:
    xbxCtrl.register_event_function('BTN_SELECT', lambda v: form.tabWidget.setCurrentIndex(form.tabWidget.currentIndex()^1) if v == 1 else None) #Select-button, changes tab !!MIGHT NOT CALL change tab!!
    register_xbx_funcs(form.tabWidget.currentIndex())


def q_change():  # only for simulation
    while True:
        if ctr.enabled:
            arm.q = np.clip(arm.q + update_dt*arm.qd, arm.q_lims[0, :], arm.q_lims[1, :]) #Encoder values. Here simulated by forward euler integration
        else:
            arm.q = arm.qr
        time.sleep(update_dt)

if SIMULATE:
    t = threading.Thread(target=q_change, daemon=True)
    t.start()


def update():  # update plot periodically
    env.robots[0].draw()
    ep.draw()

    if form.follow.isChecked():
        ctr.set_position(ep.get_pos())


# Initialize QTimer
timer = QTimer()
timer.timeout.connect(update)
timer.start(int(update_dt*1000)) #how often to update (in ms, dt is in s)

window.show()
app.exec()