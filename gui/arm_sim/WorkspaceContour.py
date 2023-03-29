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

    x_coords = []
    y_coords = []
    
    with tqdm(total=num_poses) as pbar:
        for i, a in enumerate(angles):
            pose = arm.fkine(a)
            x_coords.append(pose.t[0])
            y_coords.append(pose.t[1])
            #coords[i] = pose.t
            pbar.update(1)

    # Create 2D histogram
    H, xedges, yedges = np.histogram2d(x_coords, y_coords, bins=100)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    
    # Set vmin and vmax to increase contrast of areas with no measurements
    vmin = np.percentile(H, 10)
    vmax = np.percentile(H, 90)
    
    # Create heatmap
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(H.T, extent=extent, origin='lower', cmap='hot', vmin=vmin, vmax=vmax)
    cbar = plt.colorbar(im)
    cbar.set_label('Density')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.show()

if __name__ == "__main__":
    main()

