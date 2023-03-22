from init_robot import EiT_arm
import matplotlib.pyplot as plt
import numpy as np




def main():

    arm = EiT_arm()
    x_array = []
    y_array = []
    z_array = []

    

    angle_array = np.linspace(0,270,10) *np.pi/180
    pose = arm.fkine([0,0,0,0,0])
    
    for j in range(len(angle_array)):
        print(j/len(angle_array) * 100)
        for k in range(len(angle_array)):
            for l in range(len(angle_array)):
                for m in range(len(angle_array)):
                    for n in range(len(angle_array)):
                        pose = arm.fkine([angle_array[j],angle_array[k],angle_array[l],angle_array[m],angle_array[n]])
                      
                        x = pose.data[0][0][3]
                        y = pose.data[0][1][3]
                        z = pose.data[0][2][3]
                        x_array.append(x) 
                        y_array.append(y)
                        z_array.append(z)    


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_array,y_array , z_array, c='red', s=1)
    plt.show()
if __name__ == "__main__":
    main()