import numpy as np
import roboticstoolbox.robot as robot

class EiT_arm(robot.DHRobot):
    claw_angle = 0

    def __init__(self, q0 = None, claw0 = None):        
        links = [robot.RevoluteDH(d = 0.2, a = 0, alpha=np.pi/2),
                 robot.RevoluteDH(d = 0, a = 1/2, alpha= 0, offset=np.pi/2),
                 robot.RevoluteDH(d = 0, a = 1/2, alpha = -np.pi/2),
                 robot.RevoluteDH(d = 0, a = 0, alpha= -np.pi/2, offset= -np.pi/2),
                 robot.RevoluteDH(d = 1/8 , a = 0, alpha=0)] 
        


        super().__init__(links, name='EiT arm')      

        self.qlims = np.zeros((2, self.n))

        for i in range(self.n):
            self.qlims[:, i] = np.c_[-270/360*np.pi, 270/360*np.pi]

        if q0 is not None:
            self.q = q0          

        if claw0 is not None:
            self._claw_angle = claw0

        self.control_mode = "p"

        
        
    
    def q_degrees(self):        
        return self.q*180/np.pi


    def claw_deg(self):
        return self.claw_deg*180/np.pi


    def inverse_kinematics(self, T, verbose=True):
        T = T.A
        Ls = []
        for l in self.links:
            if l.a > 0 or l.d>0:
                Ls.append(max(l.a, l.d))

        L1, L2, L3, L4 = Ls
        
        p = T[:3, 3]
        R = T[:3, :3]

        p3 = T@np.array([0, 0, -L4, 1]).T #position of joint 3
        
        r = np.linalg.norm(p3[:2])
        s = p3[2] - L1

        q1 = np.arctan2(p3[1], p3[0]) #-pi, pi

        alpha = np.arccos((s**2 + r**2 - L2**2 - L3**2)/(2*L2*L3))
        q3 = np.pi - alpha #sign ambiguous, in 0, pi

        q2 = np.pi - np.arctan2(L3*np.abs(np.sin(q3)), L2 + L3*np.abs(np.cos(q3))) - np.arctan2(s, r)

        p2 = self.A(1, [q1, q2]).A[:3, 3] #position of joint 2

        d = np.linalg.norm(p - p2[:3])
        q4 = -np.arccos((d**2-L3**2-L4**2)/(2*L3*L4))

        R4 = self.A(3, [q1, q2, q3, q4]).A[:3, :3] #rotation matrix from world to last joint
        q5 = np.arccos((R@R4.T)[1, 1])

        T_sol = self.fkine([q1, q2, q3, q4, q5]).A

        if (not np.allclose(T_sol, T)) and verbose:          
                print("Obs! Analytical solution is not entirely correct") #due to lack of spherical wrist this analytical approach does not wprk

        return q1, q2, q3, q4, q5
    

if __name__ == "__main__":
    arm_manipulator = EiT_arm()

    # Generate random angles from -pi to pi in array of size 5
    q = np.random.random(size=5)*2*np.pi - np.pi

    q[1] = np.random.uniform(-75/90, 75/90)*np.pi/2 # Constraing the second joint to be between -75 and 75 degrees

    # q = [2.76915388, 0.45107274, 1.07980306, 2.90040424, 1.11671079]

    print('angles ground truth:', q)

    ##random pose
    arm_manipulator.q = q
    Te = arm_manipulator.fkine(arm_manipulator.q)

    print(arm_manipulator.A(0, q))

    ##analytical solution
    inv = arm_manipulator.inverse_kinematics(Te)
    print('angles analytically:', inv)

    stack = np.vstack((q, inv))
    pattern = np.tile(stack, (5, 1))

    arm_manipulator.plot(pattern, dt=1) #simulate analytical vs true

    ##numerical solution
    sol, success, iter, searches, res = arm_manipulator.ikine_LM(Te)

    if not success:
        print('could not find inverse solution numerically')
    else:
        print('angles numerically:', sol)
        arm_manipulator.plot(sol)
        input('press any key to close')