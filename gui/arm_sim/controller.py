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
        
        self.opt = Optimization_controller(arm.q_lims, arm.qd_lims)
        self.pos = Position_controller(arm.qd_lims)

        self.switch_threshold = 25*np.pi/180 #angle in rads for when to use optimization based controller

        self.T = init_pos
        self.dt = dt

        self.arrived = False

        self.mode = "Auto"
        self.active = "N/A"

    def change_mode(self, new_mode = "Auto"):
        if new_mode not in ["Auto", "Optimization", "Position"]:
            raise ValueError("Mode must be one of Auto, Optimization, Position")
        self.mode = new_mode
        self.active = "N/A"
        self.arrived = False
        print("Set controller mode to: ", new_mode)

    def set_position(self, T):
        self.T = T
        self.arrived = False

    def start(self):
        self.t = threading.Thread(target=self._control, daemon=True)
        self.t.start()        

    def _control(self):
        while True:
            while not self.arrived:
                
                Te = self.arm.fkine(self.arm.q).A
                # Calculate the base-frame manipulator Jacobian
                J0 = self.arm.jacob0(self.arm.q)

                # qd, arrived = None, None

                if self.mode == "Auto":
                    #check if close to limits for choosing which controller
                    lim_low = np.any((self.arm.q - self.arm.q_lims[0, :]) < self.switch_threshold)
                    lim_high = np.any((self.arm.q_lims[1, :] - self.arm.q) < self.switch_threshold)
                    if lim_high or lim_low:
                        if self.active != "Optimization":
                            print("Auto: Changed to Optimization controller")
                        self.active = "Optimization"
                    else:
                        if self.active != "Position":
                            print("Auto: Changed to Position controller")
                        self.active = "Position"

                if self.mode == "Optimization" or self.active == "Optimization":
                    qd, arrived = self.opt.optimization_controller(J0, Te, self.arm.q, self.T)
                    if qd is None: #optimizer failed to find a solution
                        self.active = "Position"

                if self.mode == "Position" or self.active == "Position":
                    qd, arrived = self.pos.position_controller(J0, Te, self.T)
                                
                self.arm.qd = qd

                if arrived:
                    self.arrived = True
                    break

                time.sleep(self.dt)
            time.sleep(2)