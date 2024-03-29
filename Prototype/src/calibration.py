import numpy as np
import cv2 as cv

from src.utils import distance_vr

def projection_matrices(focal_length, sensor_size, sensor_resolution, radius):
    """return left, central and right projections matrices"""

    cy, cx = sensor_resolution/2.0
    fy, fx = sensor_resolution*focal_length/(1.0*sensor_size)

    camera_matrix = np.array([[fx, 0, cx],
                              [0, fy, cy],
                              [0,  0,  1]])

    vr = distance_vr(radius)

    return (projection_matrix(camera_matrix, camera_pose_matrix(-vr)), \
            projection_matrix(camera_matrix, camera_pose_matrix(0)), \
            projection_matrix(camera_matrix, camera_pose_matrix(vr)))

def projection_matrix(camera_matrix, rotation_translation_matrix):
    """compute a projection matrix given intrinsic and extrinsic parameters"""

    return np.matmul(camera_matrix, rotation_translation_matrix)

def camera_pose_matrix(vr):
    """return extrinsic parameters computed as a translation along x-axis"""

    return np.array([[1, 0, 0,-vr],
                     [0, 1, 0,  0],
                     [0, 0, 1,  0]])
