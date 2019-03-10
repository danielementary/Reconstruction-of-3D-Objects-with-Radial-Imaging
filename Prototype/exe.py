import numpy as np
import cv2 as cv

from src.utils import angle_of_view
from src.load_save import load_image
from src.separate_views import separate_views
from src.stereo_matching import stereo_matching
from src.triangulation import triangulation
from src.recover_shape import recover_shape
from src.display_disparity_map import display_disparity_map


bread01_resized_parameters = {
    "filename" : "img/bread01/bread01_square resized (750, 750)",
    "extension" : ".JPG",
    "radius" : 35,
    "sensor_resolution" : (750, 750),
    "window_shape": (9, 9),
    "sensor_size" : (24, 24),
    "focal_length" : 24,
    "views_shape" : (375, 250),
    "bound" : 36
}

bread02_resized_parameters = {
    "filename" : "img/bread02/bread02_square resized (750, 750)",
    "extension" : ".JPG",
    "radius" : 35,
    "sensor_resolution" : (750, 750),
    "window_shape": (9, 9),
    "sensor_size" : (24, 24),
    "focal_length" : 24,
    "views_shape" : (375, 250),
    "bound" : 36
}

def execute(parameters):
    """
    """

    filename = parameters["filename"]
    extension = parameters["extension"]
    radius = parameters["radius"]
    sensor_resolution = np.array(parameters["sensor_resolution"])
    window_shape = parameters["window_shape"]
    sensor_size = np.array(parameters["sensor_size"])
    focal_length = parameters["focal_length"]
    views_shape = np.array(parameters["views_shape"])
    bound = np.array(parameters["bound"])

    theta = angle_of_view(sensor_size[1], focal_length)/2.0

    views_shape -= window_shape
    views_shape += 1

    separate_views(filename, extension, sensor_resolution)
    stereo_matching(filename, extension, window_shape, bound)
    filename += (" " + str(window_shape))
    display_disparity_map(filename)
    triangulation(filename, views_shape, focal_length, sensor_size, \
                  sensor_resolution, radius, theta)
    recover_shape(filename, views_shape)

execute(bread01_resized_parameters)
execute(bread02_resized_parameters)
