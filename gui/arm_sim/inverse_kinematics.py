import numpy as np

def inverse_kinematics(T, robot, verbose=True):
    T = T.A
    Ls = []
    for l in robot.links:
        if l.a > 0 or l.d>0:
            Ls.append(max(l.a, l.d))

    L1, L2, L3, L4 = Ls
    
    p = T[:3, 3]
    R = T[:3, :3]

    p3 = T@np.array([0, 0, -L4, 1]).T #position of joint 3
    
    r = np.linalg.norm(p3[:2])
    s = p3[2] - L1

    q1 = np.arctan2(p3[1], p3[0])
    q3 = np.arccos((s**2 + r**2 - L2**2 - L3**2)/(2*L2*L3))

    q2 = np.arctan2(L2*np.sin(-q3), L2 + L3*np.cos(q3)) + np.arctan2(s, r)

    p2 = robot.A(1, [q1, q2]).A[:3, 3] #position of joint 2
    d = np.linalg.norm(p - p2[:3])
    q4 = -np.arccos((d**2-L3**2-L4**2)/(2*L3*L4))

    R4 = robot.A(3, [q1, q2, q3, q4]).A[:3, :3] #rotation matrix from world to last joint
    q5 = np.arccos((R4.T@R)[1, 1])

    T_sol = robot.fkine([q1, q2, q3, q4, q5]).A

    if not np.allclose(T_sol, T) and verbose:
        print("Obs! Analytical solution is not entirely correct")

    return q1, q2, q3, q4, q5