import numpy as np
import cv2 as cv

from matplotlib import pyplot as plt
from matplotlib import image

def display_disparity_map(filename):
    """
    """

    left = np.load(filename+" disparity map left.npy")
    right = np.load(filename+" disparity map right.npy")

    fig = plt.figure()
    col = 2
    row = 1

    fig.add_subplot(row, col, 1)
    plt.imshow(left, cmap="gray")
    plt.title("Left")
    plt.colorbar()

    fig.add_subplot(row, col, 2)
    plt.imshow(right, cmap="gray")
    plt.title("Right")
    plt.colorbar()

    plt.show()
