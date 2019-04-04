import numpy as np
import cv2 as cv

import matplotlib.pyplot as plt
from src.calibration import projection_matrices
from src.utils import from_homogeneous_to_cartesian

def points_matrices(filename, views_shape, sensor_resolution):
    """Load and prepare point matrices to triangulate"""

    x_offset = sensor_resolution[1]/3
    y_offset = (sensor_resolution[0]-views_shape[0])/2

    _, x_indices = np.indices(views_shape)
    y_indices = np.full(views_shape, sensor_resolution[0]/2.0).flatten()

    x_indices = x_indices.flatten()

    correspondances_left = \
                          np.load(filename+" correspondance left.npy").flatten()
    correspondances_right = \
                         np.load(filename+" correspondance right.npy").flatten()

    correspondances_left = np.array((2*x_offset) + correspondances_left)
    indicex_center = np.array(x_offset + x_indices)
    correspondances_right = np.array(correspondances_right)

    points_matrix_left = np.array([correspondances_left, y_indices], \
                                  dtype=np.float)
    points_matrix_center = np.array([indicex_center, y_indices], \
                                    dtype=np.float)
    points_matrix_right = np.array([correspondances_right, y_indices], \
                                    dtype=np.float)

    return np.array([points_matrix_left, points_matrix_center, \
                                         points_matrix_right])

def triangulation(filename, views_shape, focal_length, sensor_size, \
                  sensor_resolution, radius, theta):
    """Triangulate and save points"""

    print("triangulation "+filename)

    proj_matrix_left, proj_matrix_center, proj_matrix_right = \
                           projection_matrices(focal_length, sensor_size, \
                                               sensor_resolution, radius)

    points_matrix_left, points_matrix_center, points_matrix_right = \
                       points_matrices(filename, views_shape, sensor_resolution)

    triangulated_points_homogeneous_left = \
                                cv.triangulatePoints(proj_matrix_center, \
                                                     proj_matrix_left, \
                                                     points_matrix_center, \
                                                     points_matrix_left)

    triangulated_points_homogeneous_right = \
                                cv.triangulatePoints(proj_matrix_center, \
                                                     proj_matrix_right, \
                                                     points_matrix_center, \
                                                     points_matrix_right)

    triangulated_points_cartesian_left = \
       cv.convertPointsFromHomogeneous(triangulated_points_homogeneous_left.T).T

    triangulated_points_cartesian_right = \
      cv.convertPointsFromHomogeneous(triangulated_points_homogeneous_right.T).T

    np.save(filename+" left points.npy", triangulated_points_cartesian_left)
    np.save(filename+" right points.npy", triangulated_points_cartesian_right)

    print("end triangulation "+filename)
