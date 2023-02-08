import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from matplotlib.widgets import Slider, RadioButtons


L = [1/2, 1.5, 1.5, 1]
q = np.array([10, 20, 30, -90, 50])*np.pi/180
current_q = 0 #what q is activated to rotate about in ui

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')

def translate_xyz(x, y, z):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]])

def rotate_z(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                     [np.sin(angle), np.cos(angle), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

def rotate_y(angle):
    return np.array([[np.cos(angle), 0, np.sin(angle), 0],
                     [0, 1, 0, 0],
                     [-np.sin(angle), 0, np.cos(angle), 0],
                     [0, 0, 0, 1]])

def rotate_x(angle):
    return np.array([[1, 0, 0, 0],
                     [0, np.cos(angle), -np.sin(angle), 0],
                     [0, np.sin(angle), np.cos(angle), 0],
                     [0, 0, 0, 1]])


def DH_transform(d, theta, a, alpha):
    return rotate_z(theta)@translate_xyz(0, 0, d)@rotate_x(alpha)@translate_xyz(a, 0, 0)


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


def draw_arm(ax):
    ax.clear()
    #define frames
    f1 = DH_transform(d=L[0], theta=q[0], alpha=np.pi/2, a = 0)
    f2 = f1@DH_transform(d=0, theta=q[1], alpha=0, a=L[1])
    f3 = f2@DH_transform(d=0, theta=q[2], alpha=-np.pi/2, a=L[2])
    f4 = f3@DH_transform(d=0, theta=q[3], alpha=-np.pi/2, a=0)
    f5 = f4@DH_transform(d=L[3], theta=q[4], alpha=0, a=0)
    #world frame
    draw_frame(np.eye(4), ax)
    #joint frames
    for f in [f1, f2, f3, f4, f5]:
        draw_frame(f, ax)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(0, 5)


fig.subplots_adjust(bottom=0.25, left=0.25)

chk_box = fig.add_axes([0.05, 0.4, 0.1, 0.15])
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