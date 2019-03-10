import numpy as np
import cv2 as cv

from matplotlib import pyplot as plt

THRESHOLD = 20

def filter_valid_matches(filename, views_shape):
    """
    """

    print("filter "+filename)

    left_points = np.load(filename+" left points.npy")
    right_points = np.load(filename+" right points.npy")

    filter_matrix = np.empty(views_shape)

    confidence_distances = left_points-right_points

    filter_matrix[np.absolute(confidence_distances[2]).reshape(views_shape) <= THRESHOLD] = 1
    filter_matrix[np.absolute(confidence_distances[2]).reshape(views_shape) > THRESHOLD] = 0

    print(filter_matrix)

    display_distances(left_points, right_points, filter_matrix, views_shape)

    left_points *= filter_matrix.flatten()
    right_points *= filter_matrix.flatten()

    np.save(filename+" filtered left points.npy", left_points)
    np.save(filename+" filtered right points.npy", right_points)

    print("end filter "+filename)

def display_distances(left_points, right_points, filter_matrix, views_shape):
    """
    """

    difference = left_points-right_points

    fig = plt.figure()
    col = 3
    row = 1

    fig.add_subplot(row, col, 1)
    plt.imshow(np.absolute(difference[0]).reshape(views_shape), cmap="gray")
    plt.title("X-axis")
    plt.colorbar()

    fig.add_subplot(row, col, 2)
    plt.imshow(np.absolute(difference[1]).reshape(views_shape), cmap="gray")
    plt.title("Y-axis")
    plt.colorbar()

    fig.add_subplot(row, col, 3)
    plt.imshow(np.absolute(difference[2]).reshape(views_shape), cmap="gray")
    plt.title("Z-axis")
    plt.colorbar()

    plt.show()
