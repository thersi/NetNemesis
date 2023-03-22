from init_robot import EiT_arm
import matplotlib.pyplot as plt
import numpy as np
import itertools

def main():
    arm = EiT_arm()

    angle_array = np.linspace(0, 270, 10) * np.pi / 180

    angles = itertools.product(angle_array, repeat=5)
    poses = [arm.fkine(a) for a in angles]

    coords = np.array([p.t for p in poses])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c='red', s=1)
    plt.show()

if __name__ == "__main__":
    main()
