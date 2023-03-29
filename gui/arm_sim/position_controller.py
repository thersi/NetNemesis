import numpy as np
import roboticstoolbox as rtb


class Position_controller:
    """
    A controller for postions and rotation of the arm. Using Postion Based Servoing for finding wanted velocity
    and using the manipulator jacobian for computing joint angles.
    Due to 5 DOF's and 6 paramters to control, we do not have a nullspace to use for nullspace projection.
    Instability, critical configurations and impossible end goals might occur.
    """

    def __init__(self, qdlim, kt=2, kr=1):
        self.k = np.array([kt, kt, kt, kr, kr, kr])
        self.qdlim = qdlim


    def _joint_velocity(self, J0, ev):
        """
        Calculates the required joint velocities qd to achieve the desired
        end-effector velocity ev.

        ev: the desired end-effector velocity (expressed in the base-frame
            of the robot)
        """
        
        # Calculate the pseudoinverse of the base-frame manipulator Jacobian
        J0_pinv = np.linalg.pinv(J0)
        qd = J0_pinv @ ev

        return qd


    def position_controller(self, J0, Te, qs, goal):
        # Calculate the required end-effector velocity and whether the robot has arrived
        ev, arrived = rtb.p_servo(Te, goal, gain=self.k, threshold=0.01, method="angle-axis")
        if arrived:
            n = len(qs)
            return np.zeros(n), True

        # Calculate the required joint velocities and apply to the robot
        qd =  self._joint_velocity(J0, ev)

        #should limit qd here, psuedoinverse can give huge qds
        qd_limited = np.clip(qd, self.qdlim[0, :], self.qdlim[1, :])

        return qd_limited, arrived
