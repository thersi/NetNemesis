import numpy as np
import roboticstoolbox as rtb                         
import qpsolvers as qp # this package provides several solvers for solving quadratic programmes
import threading
import time

from arm_sim.init_robot import EiT_arm


class optimization_controller:
    """
    A controller for postions and rotation of the arm. Using Postion Based Servoing and quadratic programming

    The controller is launched in new thread, and new values for position and rotation is set using the set_pos method
    """

    def __init__(self, robot : EiT_arm, ps : float = 0.05, pi: float = 0.9, vel_gain: float = 1.0, servo_gain_t : float = 1.0, servo_gain_r=1.3):
        """
        ps: The minimum angle (in radians) in which the joint is
            allowed to approach to its limit
        pi: The influence angle (in radians) in which the velocity
            damper becomes active
        vel_gain: The gain for the velocity damper
        servo_gain_t: The gain for the p_servo method for translation
        servo_gain_r: The gain for the p_servo method for rotation
        """

        self.robot = robot
        self.goal = robot.fkine(robot.q).A
        self.arrived = True

        self.ps = ps
        self.pi = pi
        self.gain = vel_gain

        self.k = np.array([servo_gain_t, servo_gain_t, servo_gain_t, servo_gain_r, servo_gain_r, servo_gain_r])


    def start(self, dt):
        self.t = threading.Thread(target=self.optimization_controller, args = [dt], daemon = True)
        self.t.start()

    
    def _joint_velocity_damper(self):
        """
        Formulates an inequality contraint which, when optimised for will
        make it impossible for the robot to run into joint limits. Requires
        the joint limits of the robot to be specified.

        returns: Ain, Bin as the inequality contraints for an qp
        """

        Ain = np.zeros((self.robot.n, self.robot.n))
        Bin = np.zeros(self.robot.n)

        for i in range(self.robot.n):
            if self.robot.q[i] - self.robot.qlims[0, i] <= self.pi:
                Bin[i] = -self.gain * (((self.robot.qlims[0, i] - self.robot.q[i]) + self.ps) / (self.pi - self.ps))
                Ain[i, i] = -1
            if self.robot.qlims[1, i] - self.robot.q[i] <= self.pi:
                Bin[i] = self.gain * ((self.robot.qlims[1, i] - self.robot.q[i]) - self.ps) / (self.pi - self.ps)
                Ain[i, i] = 1

        return Ain, Bin

    

    def set_pos(self, T_goal):
        """
        Set the goal axes for the end effector

        T_goal: wanted postion and orientation as 4x4 np.narray
        """
        self.goal = T_goal
        self.arrived = False


    def optimization_controller(self, dt):        
        # Set the gain on the manipulability maximisation
        # λm = 1.0
        # Set the gain on the joint velocity norm minimisation
        λq = 0.1

        # Make a variable for the upper and lower limits of the robot
        qd_lb = -20.0*np.ones(self.robot.n)
        qd_ub = 20.0*np.ones(self.robot.n)

        while True:
            # Run the simulation until the robot arrives at the goal
            while not self.arrived:
                # Work out the base frame manipulator Jacobian using the current robot configuration
                J = self.robot.jacob0(self.robot.q)     

                # Calculate the manipulability Jacobian
                # Jm = panda.jacobm(panda.q, axes='rot')                     

                # The end-effector pose of the panda (using .A to get a numpy array instead of an SE3 object)
                Te = self.robot.fkine(self.robot.q).A

                # Spatial error
                e = np.sum(np.abs(rtb.angle_axis(Te, self.goal)))

                # Calculate the required end-effector velocity and whether the robot has arrived
                ev, self.arrived = rtb.p_servo(Te, self.goal, gain=self.k, threshold=0.001, method="angle-axis")

                ### Calculate each component of the quadratic programme
                # Quadratic component of objective function
                Q = np.eye(self.robot.n + 6)

                # Joint velocity component of Q
                Q[:self.robot.n, :self.robot.n] *= λq

                # Slack component of Q
                Q[self.robot.n:, self.robot.n:] = (1 / e) * np.eye(6)

                # The equality contraints
                Aeq = np.c_[J, np.eye(6)]
                beq = ev.reshape((6,))

                # The inequality constraints for joint limit avoidance
                Ain = np.zeros((self.robot.n + 6, self.robot.n + 6))
                bin = np.zeros(self.robot.n + 6)

                # Form the joint limit velocity damper
                Ain[:self.robot.n, :self.robot.n], bin[:self.robot.n] = self._joint_velocity_damper()

                # Linear component of objective function: the manipulability Jacobian, but have no manipulability so is zero
                # c = np.r_[λm * -Jm.reshape((panda.n,)), np.zeros(6)]
                c = np.zeros(self.robot.n + 6)

                # The lower and upper bounds on the joint velocity and slack variable
                lb = np.r_[qd_lb, -10 * np.ones(6)]
                ub = np.r_[qd_ub, 10 * np.ones(6)]

                # Solve for the joint velocities qd and apply to the robot
                xd = qp.solve_qp(Q, c, Ain, bin, Aeq, beq, lb=lb, ub=ub, solver='quadprog')

                # Apply the joint velocities to the Panda
                if xd is not None:
                    self.robot.qd[:self.robot.n] = xd[:self.robot.n]  

                time.sleep(dt)
            time.sleep(0.5)


if __name__ == "__main__":
    # Make the environment
    arm = EiT_arm()
    env = rtb.backends.PyPlot.PyPlot()
    env.launch(realtime=True)
    env.add(arm)

    dt = 0.05

    ctr = optimization_controller(arm)
    ctr.set_pos(arm.fkine([1, 0, 1, 0, 1]).A)
    ctr.start(dt)

    # Change the robot configuration to a ready position
    arm.q = [0.21, -0.03, 0.35, -1.90, -0.04]

    flag = False
    while True:
        arm.q = arm.q + dt*(arm.qd) #get encoder values. Here simulated perfectly (no noise)
        env.step(dt) #update plot

        if ctr.arrived:
            if flag:
                ctr.set_pos(arm.fkine([1, 0, 1, 0, 1]).A)
            else:
                ctr.set_pos(arm.fkine([0.61, -0.03, 0.35, -1.90, -0.04]).A)
            flag = not flag
            