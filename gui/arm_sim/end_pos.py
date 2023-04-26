import numpy as np
import matplotlib.patheffects as PathEffects
from arm_sim.transform import *

class EndPosition:
    drawn = False

    def __init__(self, T0, ax, scale=1/24, labels=True, reach = 1.2):
        self.T = T0
        self.ax = ax
        self.scale = scale
        self.labels = labels
        self.enabled = True
        self.reach = reach

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def set_pos(self, T):
        if np.linalg.norm(T[:3, 3]) < self.reach:
            self.T = T

    def get_pos(self):
        return self.T

    def translate(self, dx, dy, dz): #along own axes
        newT = self.T@translate_xyz(dx, dy, dz)
        if np.linalg.norm(newT[:3, 3]) < self.reach:
            self.T = newT

    def rotate(self, ax, ay, az): #rotate about own axes
        self.T = self.T@rotate_x(ax)@rotate_y(ay)@rotate_z(az)

    def draw(self):
        if not self.enabled:
            if self.drawn: #need to remove from plot

                for a in self.axes:
                    a.remove()
                del self.axes

                if self.labels:
                    for l in self.txts:
                        l.remove()
                    del self.txts

                self.drawn = False
            return
        
        if not self.drawn:
            self._draw_first()
            return

        X = self.T@np.asarray([[0, self.scale, 0, 0], [0, 0, self.scale, 0], [0, 0, 0, self.scale], [1, 1, 1, 1]])  

        for i, a in enumerate(self.axes):
            a.set_xdata([X[0, 0], X[0, i + 1]])
            a.set_ydata([X[1, 0], X[1, i + 1]])
            a.set_3d_properties([X[2, 0], X[2, i + 1]])

        if self.labels:
            for i, l in enumerate(self.txts):
                l.set_position_3d((X[0, i+1], X[1, i+1], X[2, i+1]))

    def _draw_first(self):
        X = self.T@np.asarray([[0, self.scale, 0, 0], [0, 0, self.scale, 0], [0, 0, 0, self.scale], [1, 1, 1, 1]])  

        self.axes = []

        self.axes.append(self.ax.plot([X[0, 0], X[0, 1]], [X[1, 0], X[1, 1]], [X[2, 0], X[2, 1]], color='#cc4422')[0]) # X-axis
        self.axes.append(self.ax.plot([X[0, 0], X[0, 2]], [X[1, 0], X[1, 2]], [X[2, 0], X[2, 2]], color='#11ff33')[0]) # Y-axis
        self.axes.append(self.ax.plot([X[0, 0], X[0, 3]], [X[1, 0], X[1, 3]], [X[2, 0], X[2, 3]], color='#3366ff')[0]) # Z-axis

        if self.labels:
            self.txts = []

            textargs = {'color': 'w', 'va': 'center', 'ha': 'center', 'fontsize': 'x-small', 'path_effects': [PathEffects.withStroke(linewidth=1.5, foreground='k')]}

            self.txts.append(self.ax.text(X[0, 1], X[1, 1], X[2, 1], 'X', **textargs))
            self.txts.append(self.ax.text(X[0, 2], X[1, 2], X[2, 2], 'Y', **textargs))
            self.txts.append(self.ax.text(X[0, 3], X[1, 3], X[2, 3], 'Z', **textargs))

        self.drawn = True

    def __repr__(self):
        return str(self.T)