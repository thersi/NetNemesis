import numpy as np
import roboticstoolbox as rtb


class Position_controller:
    """
    A controller for postions and rotation of the arm. Using Postion Based Servoing for finding wanted velocity
    and using the manipulator jacobian for computing joint angles.
    Due to 5 DOF's and 6 paramters to control, we do not have a nullspace to use for nullspace projection.
    Instability, critical configurations and impossible end goals might occur.

    The controller is launched in new thread, and new values for position and rotation is set using the set_pos method
    """

    def __init__(self, kt=1.0, kr=1.3):
        self.k = np.array([kt, kt, kt, kr, kr, kr])


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


    def position_controller(self, J0, Te, goal):
        # Calculate the required end-effector velocity and whether the robot has arrived
        ev, arrived = rtb.p_servo(Te, goal, gain=self.k, threshold=0.001, method="angle-axis")

        # Calculate the required joint velocities and apply to the robot
        return self._joint_velocity(J0, ev), arrived
