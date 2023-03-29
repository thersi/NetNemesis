import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from matplotlib.widgets import Slider, RadioButtons
from gui.arm_sim.transform import *

##DH params
L = [1/2, 1.5, 1.5, 1]
q = np.array([0, 0, 0, 0, 0])*np.pi/180

current_q = 0 #what q is activated to rotate about in ui

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')

def draw_frame(T, ax, scale=1/2, labels=True):

    X = T @ np.array([
                    [0,scale,0,0],
                    [0,0,scale,0],
                    [0,0,0,scale],
                    [1,1,1,1]])

    
    ax.plot3D([X[0, 0], X[0, 1]], [X[1, 0], X[1, 1]], [X[2, 0], X[2, 1]], color='#cc4422') # X-axis
    ax.plot3D([X[0, 0], X[0, 2]], [X[1, 0], X[1, 2]], [X[2, 0], X[2, 2]], color='#11ff33') # Y-axis
    ax.plot3D([X[0, 0], X[0, 3]], [X[1, 0], X[1, 3]], [X[2, 0], X[2, 3]], color='#3366ff') # Z-axis

    if labels:
        textargs = {'color': 'w', 'va': 'center', 'ha': 'center', 'fontsize': 'x-small', 'path_effects': [PathEffects.withStroke(linewidth=1.5, foreground='k')]}
        ax.text(X[0, 1], X[1, 1], X[2, 1], 'X', **textargs)
        ax.text(X[0, 2], X[1, 2], X[2, 2], 'Y', **textargs)
        ax.text(X[0, 3], X[1, 3], X[2, 3], 'Z', **textargs)


def draw_link(ax, frame, prev_link):
    pos = frame@np.array([0, 0, 0, 1]).T
    ax.plot3D([prev_link[0], pos[0]],[prev_link[1], pos[1]],[prev_link[2], pos[2]],color='#121212')
    return pos

def draw_arm(ax):
    ax.clear()
    #define frame transforms, follow defined DH-table
    f1 = DH_transform(d=L[0], theta=q[0], alpha=np.pi/2, a = 0)
    f2 = f1@DH_transform(d=0, theta=q[1]+np.pi/2, alpha=0, a=L[1])
    f3 = f2@DH_transform(d=0, theta=q[2], alpha=-np.pi/2, a=L[2])
    f4 = f3@DH_transform(d=0, theta=q[3]-np.pi/2, alpha=-np.pi/2, a=0)
    f5 = f4@DH_transform(d=L[3], theta=q[4], alpha=0, a=0)
    #world frame
    draw_frame(np.eye(4), ax)
    #joint frames
    link_start = np.zeros(4)
    for f in [f1, f2, f3, f4, f5]:
        draw_frame(f, ax)
        link_start = draw_link(ax, f, link_start)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(0, 5)


fig.subplots_adjust(bottom=0.25)

chk_box = fig.add_axes([0.10, 0.4, 0.1, 0.2])
labels = ["$q_1$", "$q_2$", "$q_3$", "$q_4$", "$q_5$"]
radio = RadioButtons(chk_box, labels)
radio.value_selected = labels[current_q]

slider_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03])
q_slider = Slider(ax=slider_ax, label=f'$q_{current_q + 1}$ in degrees', valmin=-100, valmax=100, valinit=q[current_q]*180/np.pi, orientation='horizontal')

def update_q(new_val):
    q[current_q] = new_val*np.pi/180
    draw_arm(ax)

def check_click(label):
    global current_q
    new_q = labels.index(label) 
    current_q = new_q
    q_slider.label.set_text(f'$q_{current_q + 1}$ in degrees')
    q_slider.set_val(q[current_q]*180/np.pi)

radio.on_clicked(check_click)
q_slider.on_changed(update_q)

draw_arm(ax)
plt.show()