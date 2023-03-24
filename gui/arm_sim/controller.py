import numpy as np
import threading
import time

from arm_sim.optimization_controller import Optimization_controller
from arm_sim.position_controller import Position_controller


class Controller:
    """
    Implements both controller types and chooses what output to use. Optimization is chosen when joint angles are close to limit.
    Else straight line controller is implemented.
    """
    def __init__(self, arm, init_pos, dt):
        self.arm = arm
        self.opt = Optimization_controller(arm.qlims)
        self.pos = Position_controller()

        self.T = init_pos
        self.dt = dt
        self.enabled = True

        self.arrived = False

        self.active = "Position"

    def set_position(self, T):
        self.T = T
        self.arrived = False

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def start(self):
        self.t = threading.Thread(target=self._control, daemon=True)
        self.t.start()        

    def _control(self):
        while True:
            while not self.arrived:

                if not self.enabled:
                    break

                Te = self.arm.fkine(self.arm.q).A
                # Calculate the base-frame manipulator Jacobian
                J0 = self.arm.jacob0(self.arm.q)

                qd1, arrived1 = self.pos.position_controller(J0, Te, self.T)
                qd2, arrived2 = self.opt.optimization_controller(J0, Te, self.arm.q, self.T)

                if arrived1 or arrived2:
                    self.arrived = True
                    self.arm.qd = np.zeros(self.arm.n)
                    break

                if qd2 is None: #the optimizer might not find a solution
                    self.arm.qd = qd1
                else:                    #logic for choosing qds
                    minv = 0.5

                    lim_low = min(self.arm.q - self.arm.qlims[0, :]) < minv
                    lim_high = min(self.arm.qlims[1, :] - self.arm.q) < minv
                    
                    if lim_low or lim_high: #optimization
                        self.arm.qd = qd2

                        if self.active == "Position":
                            print("Changed to Optimization")
                            self.active = "Optimization"
                    else:
                        self.arm.qd = qd1

                        if self.active == "Optimization":
                            print("Changed to Position")
                            self.active = "Position"

                time.sleep(self.dt)

            time.sleep(2)