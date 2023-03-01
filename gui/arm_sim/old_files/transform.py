import numpy as np

def translate_xyz(x, y, z):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]])

def rotate_z(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                     [np.sin(angle), np.cos(angle), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

def rotate_y(angle):
    return np.array([[np.cos(angle), 0, np.sin(angle), 0],
                     [0, 1, 0, 0],
                     [-np.sin(angle), 0, np.cos(angle), 0],
                     [0, 0, 0, 1]])

def rotate_x(angle):
    return np.array([[1, 0, 0, 0],
                     [0, np.cos(angle), -np.sin(angle), 0],
                     [0, np.sin(angle), np.cos(angle), 0],
                     [0, 0, 0, 1]])


def DH_transform(d, theta, a, alpha):
    return rotate_z(theta)@translate_xyz(0, 0, d)@rotate_x(alpha)@translate_xyz(a, 0, 0)