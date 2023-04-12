import numpy as np
import roboticstoolbox as rtb                         
import qpsolvers as qp # this package provides several solvers for solving quadratic programmes


class Optimization_controller:
    """
    A controller for postions and rotation of the arm. Using Postion Based Servoing and quadratic programming

    The controller is launched in new thread, and new values for position and rotation is set using the set_pos method
    """

    def __init__(self, qlim, qdlim):
        #ps: The minimum angle (in radians) in which the joint is allowed to approach to its limit
        self.ps = 0.05
        #pi: The influence angle (in radians) in which the velocity damper becomes active
        self.pi = 0.5
        #The gain for the velocity damper
        self.gain = 1.0

        # Set the gain on the joint velocity norm minimisation
        self.λq = 0.5

        # Make a variable for the upper and lower limits of the robot angle velocities
        self.qd_lb = qdlim[0, :]
        self.qd_ub = qdlim[1, :]
        #The gain for the p_servo method for translation
        kt = 2
        #The gain for the p_servo method for rotation
        kr = 1
        self.k = np.array([kt, kt, kt, kr, kr, kr])

        self.qlim = qlim

    
    def _joint_velocity_damper(self, qs):
        """
        Formulates an inequality contraint which, when optimised for will
        make it impossible for the robot to run into joint limits. Requires
        the joint limits of the robot to be specified.

        returns: Ain, Bin as the inequality contraints for an qp
        """
        n = len(qs)
        Ain = np.zeros((n, n))
        Bin = np.zeros(n)

        for i in range(n):
            if qs[i] - self.qlim[0, i] <= self.pi:
                Bin[i] = -self.gain * (((self.qlim[0, i] - qs[i]) + self.ps) / (self.pi - self.ps))
                Ain[i, i] = -1
            if self.qlim[1, i] - qs[i] <= self.pi:
                Bin[i] = self.gain * ((self.qlim[1, i] - qs[i]) - self.ps) / (self.pi - self.ps)
                Ain[i, i] = 1

        return Ain, Bin


    def optimization_controller(self, J, Te, qs, goal):        
        n = len(qs)
        # Calculate the manipulability Jacobian #not done due to no extra degrees of freedom so no extra manipulabilty
        # Jm = panda.jacobm(panda.q, axes='rot')                     

        # Spatial error
        e = np.sum(np.abs(rtb.angle_axis(Te, goal)))
        # e = np.linalg.norm(Te[:3, 3] - goal[:3, 3])

        # Calculate the required end-effector velocity and whether the robot has arrived
        ev, arrived = rtb.p_servo(Te, goal, gain=self.k, threshold=0.01, method="angle-axis")

        if arrived:            
            return np.zeros(n), True

        ### Calculate each component of the quadratic programme
        # Quadratic component of objective function
        Q = np.eye(n + 6)

        # Joint velocity component of Q
        Q[:n, :n] *= self.λq

        # Slack component of Q
        Q[n:, n:] = (1 / e) * np.eye(6)

        # The equality contraints
        Aeq = np.c_[J, np.eye(6)]
        beq = ev.reshape((6,))

        # The inequality constraints for joint limit avoidance
        Ain = np.zeros((n + 6, n + 6))
        bin = np.zeros(n + 6)

        # Form the joint limit velocity damper
        Ain[:n, :n], bin[:n] = self._joint_velocity_damper(qs)

        # Linear component of objective function: the manipulability Jacobian, but have no manipulability so is zero
        # c = np.r_[λm * -Jm.reshape((n,)), np.zeros(6)]
        c = np.zeros(n + 6)

        # The lower and upper bounds on the joint velocity and slack variable
        lb = np.r_[self.qd_lb, -10 * np.ones(6)]
        ub = np.r_[self.qd_ub, 10 * np.ones(6)]

        # Solve for the joint velocities qd and apply to the robot
        xd = qp.solve_qp(Q, c, Ain, bin, Aeq, beq, lb=lb, ub=ub, solver='quadprog')

        if xd is not None:
            return xd[:n], arrived
        return None, None
