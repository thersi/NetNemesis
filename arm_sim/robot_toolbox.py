from swift import Swift
import roboticstoolbox as rtb
import spatialmath as sm
import numpy as np
import spatialgeometry as sg

# Make the environment
env = Swift()

# Launch the simulator, will open a browser tab in your default
# browser (chrome is recommended)
# The realtime flag will ask the simulator to simulate as close as
# possible to realtime as apposed to as fast as possible
env.launch(realtime=True)
env.set_camera_pose([1.3, 0, 0.4], [0, 0, 0.3])

# Note that everytime this cell is run, a new browser tab will open
# Make a panda robot
panda = rtb.models.Panda()

# Set the joint coordinates to qr
panda.q = panda.qr

# We can then add our robot to the simulator envionment
env.add(panda)

# end-effector axes
ee_axes = sg.Axes(0.1)

# goal axes
goal_axes = sg.Axes(0.1)

# Add the axes to the environment
env.add(ee_axes)
env.add(goal_axes) 


def null_project(robot, q, qnull, ev, λ):
    """
    Calculates the required joint velocities qd to achieve the desired
    end-effector velocity ev while projecting the null-space motion qnull
    into the null-space of the jacobian of the robot.

    robot: a Robot object (must be redundant with robot.n > 6)
    q: the robots current joint coordinates
    qnull: the null-space motion to be projected into the solution
    ev: the desired end-effector velocity (expressed in the base-frame
        of the robot)
    λ: a gain to apply to the null-space motion

    Note: If you would like to express ev in the end-effector frame,
        change the `jacob0` below to `jacobe`
    """

    # Calculate the base-frame manipulator Jacobian
    J0 = robot.jacob0(q)

    # Calculate the pseudoinverse of the base-frame manipulator Jacobian
    J0_pinv = np.linalg.pinv(J0)

    # Calculate the joint velocity vector according to the equation above
    qd = J0_pinv @ ev + (1.0 / λ) * (np.eye(robot.n) - J0_pinv @ J0) @ qnull.reshape(robot.n,)

    return qd

def jacobm(robot, q, axes):
    """
    Calculates the manipulability Jacobian. This measure relates the rate
    of change of the manipulability to the joint velocities of the robot.

    q: The joint angles/configuration of the robot
    axes: A boolean list which correspond with the Cartesian axes to
        find the manipulability Jacobian of (6 boolean values in a list)

    returns the manipulability Jacobian
    """

    # Calculate the base-frame manipulator Jacobian
    J0 = robot.jacob0(q)

    # only keep the selected axes of J
    J0 = J0[axes, :]

    # Calculate the base-frame manipulator Hessian
    H0 = robot.hessian0(q)

    # only keep the selected axes of H
    H0 = H0[:, axes, :]

    # Calculate the manipulability of the robot
    manipulability = np.sqrt(np.linalg.det(J0 @ J0.T))

    # Calculate component of the Jacobian
    b = np.linalg.inv(J0 @ J0.T)

    # Allocate manipulability Jacobian
    Jm = np.zeros((robot.n, 1))

    # Calculate manipulability Jacobian
    for i in range(robot.n):
        c = J0 @ H0[i, :, :].T
        Jm[i, 0] = manipulability * (c.flatten("F")).T @ b.flatten("F")

    return Jm



# Change the robot configuration to a ready position
panda.q = [0.21, -0.03, 0.35, -1.90, -0.04, 1.96, 1.36]

# Only the translation axes
trans_axes = [True, True, True, False, False, False]
# Only the rotation aces
rot_axes = [False, False, False, True, True, True]

# All axes
all_axes = [True, True, True, True, True, True]

# Step the sim to view the robot in this configuration
env.step(0)

# A variable to specify when to break the loop
arrived = False

# Specify our timestep
dt = 0.05

Tep = (
    panda.fkine(panda.q)
    * sm.SE3.Tx(-0.1)
    * sm.SE3.Ty(0.6)
    * sm.SE3.Tz(0.4)
)
Tep = Tep.A

# Set the goal axes to Tep
goal_axes.T = Tep

# Set the gain on the manipulability maximisation
λ = 0.1

# Specify the gain for the p_servo method
kt = 1.0
kr = 1.3
k = np.array([kt, kt, kt, kr, kr, kr])

# Run the simulation until the robot arrives at the goal
while not arrived:

    # Work out the base frame manipulator Jacobian using the current robot configuration
    J = panda.jacob0(panda.q)

    # Calculate the desired null-space motion
    qnull = jacobm(panda, panda.q, trans_axes)

    # The end-effector pose of the panda (using .A to get a numpy array instead of an SE3 object)
    Te = panda.fkine(panda.q).A

    # Calculate the required end-effector velocity and whether the robot has arrived
    ev, arrived = rtb.p_servo(Te, Tep, gain=k, threshold=0.001, method="angle-axis")

    # Calculate the required joint velocities and apply to the robot
    panda.qd = null_project(panda, panda.q, qnull, ev, λ)

    # Update the ee axes
    ee_axes.T = Te

    # Step the simulator by dt seconds
    env.step(dt)