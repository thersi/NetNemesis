from init_robot import EiT_arm
import matplotlib.pyplot as plt
import numpy as np
import itertools
from tqdm import tqdm

def main():
    arm = EiT_arm()

    angle_array = np.linspace(-135, 135, 15) * np.pi / 180

    angles = itertools.product(angle_array, repeat=5)
    num_poses = len(angle_array) ** 5

    coords = np.zeros((num_poses, 3))
    with tqdm(total=num_poses) as pbar:
        for i, a in enumerate(angles):
            pose = arm.fkine(a)
            coords[i] = pose.t
            pbar.update(1)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c='red', s=1)
    plt.show()

if __name__ == "__main__":
    main()
