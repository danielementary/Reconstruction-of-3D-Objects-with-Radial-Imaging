#this is a standalon script created to ensure that everything runs as expected

import numpy as np
import cv2 as cv

from src.calibration import projection_matrices

def get_2d_point(point_3d_homogeneous, projection_matrix):
    """Convert a 3d homogeneous coordinates point
       to a 2d euclidean coordinates"""

    temp = np.matmul(projection_matrix, point_3d_homogeneous)

    return cv.convertPointsFromHomogeneous(np.array([temp], np.float))

#used camera intrinsic parameters for testing
radius = 35
sensor_resolution = np.array([3744, 3744])
sensor_size = np.array([24, 24])
focal_length = 24

#geometry testing

list_point_3d_homogeneous = [(0, 0, 140, 1), (0, 0, 210, 1), (0, 0, 420, 1)]

projection_matrix_left, projection_matrix_center, projection_matrix_right = \
       projection_matrices(focal_length, sensor_size, sensor_resolution, radius)

for p in list_point_3d_homogeneous:
    print(p)
    print(get_2d_point(p, projection_matrix_left))
    print(get_2d_point(p, projection_matrix_center))
    print(get_2d_point(p, projection_matrix_right))


#triangulation testing

left_m = np.array([[3744, 3120, 2496],
                   [1872, 1872, 1872]], np.float)

central_m = np.array([[1872, 1872, 1872],
                      [1872, 1872, 1872]], np.float)

right_m = np.array([[0, 624, 1248],
                    [1872, 1872, 1872]], np.float)

points_left = cv.triangulatePoints(projection_matrix_left, \
                                    projection_matrix_center, left_m, central_m)
points_right = cv.triangulatePoints(projection_matrix_center, \
                                    projection_matrix_right, central_m, right_m)

points_left = cv.convertPointsFromHomogeneous(points_left.T)
points_right = cv.convertPointsFromHomogeneous(points_right.T)

print("left")
print(points_left)

print("right")
print(points_right)
