import numpy as np
from init_robot import EiT_arm
import roboticstoolbox as rt
import threading
import time

class arm_controller:
    """
    A controller for postions and rotation of the arm. Using Postion Based Servoing for finding wanted velocity
    and using the manipulator jacobian for computing joint angles.
    Due to 5 DOF's and 6 paramters to control, we do not have a nullspace to use for nullspace projection.
    Instability, critical configurations and impossible end goals might occur.

    The controller is launched in new thread, and new values for position and rotation is set using the set_pos method
    """

    def __init__(self, robot : EiT_arm):
        self.robot = robot
        self.goal = robot.fkine(robot.q).A
        self.arrived = True      
        # self.t = threading.Thread(target=self.start_controller, daemon = True)
        # self.t.start()

    def control_loop(self, gain):
        # The end-effector pose of the arm
        Te = self.robot.fkine(self.robot.q).A

        # Calculate the required end-effector velocity and whether the robot has arrived
        ev, arrived = rt.p_servo(Te, self.goal, gain=gain, threshold=0.001, method="angle-axis")

        # Calculate the required joint velocities and apply to the robot
        return self.joint_velocity(ev), arrived


    
    def joint_velocity(self, ev):
        """
        Calculates the required joint velocities qd to achieve the desired
        end-effector velocity ev.

        ev: the desired end-effector velocity (expressed in the base-frame
            of the robot)
        """

        # Calculate the base-frame manipulator Jacobian
        J0 = self.robot.jacob0(self.robot.q)
        # Calculate the pseudoinverse of the base-frame manipulator Jacobian
        J0_pinv = np.linalg.pinv(J0)
        qd = J0_pinv @ ev #+ (1.0 / λ) * (np.eye(robot.n) - J0_pinv @ J0) @ qnull.reshape(robot.n,)

        return qd
    

    def set_pos(self, T_goal):
        """
        Set the goal axes for the end effector

        T_goal: wanted postion and orientation as 4x4 np.narray
        """
        self.goal = T_goal
        self.arrived = False


    def start_controller(self):
        # Specify the gain for the p_servo method
        kt = 1.0
        kr = 1.3
        k = np.array([kt, kt, kt, kr, kr, kr])

        # Run the simulation until the robot arrives at the goal
        while True:
            while not self.arrived:
                # The end-effector pose of the arm
                Te = self.robot.fkine(self.robot.q).A

                # Calculate the required end-effector velocity and whether the robot has arrived
                ev, self.arrived = rt.p_servo(Te, self.goal, gain=k, threshold=0.001, method="angle-axis")

                # Calculate the required joint velocities and apply to the robot
                self.robot.qd = self.joint_velocity(ev)
                print('ev', ev)
                time.sleep(0.1)       
            print("arrived")     
            time.sleep(0.5)