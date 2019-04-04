import numpy as np
import cv2 as cv

from src.load_save import load_image, save_three_views, save_merged_views
from src.utils import resize

def separate_views(filename, ext, sensor_resolution):
    """Separate left, central and right views from a radial image"""

    print("views separation " + filename)

    image = load_image(filename, ext)
    side = sensor_resolution[0]
    steps = int(side/2)
    alpha = angle_alpha(steps)

    virtual_width, real_width = virtual_real_lengths(side)

    left_view = np.empty((steps, virtual_width, 3))
    central_view = np.empty((steps, real_width, 3))
    right_view = np.empty((steps, virtual_width, 3))

    for s in range(steps):
        slice = take_slice(s, alpha, image, side)
        JK, KL, LM = split_slice(slice, virtual_width, real_width)
        left_view[s] = JK[::-1]
        central_view[s] = KL
        right_view[s] = LM[::-1]

    save_three_views(filename, ext, left_view, central_view, right_view)
    save_merged_views(filename, ext, left_view, central_view, right_view)

    print("end views separation " + filename)

def angle_alpha(steps):
    return np.pi/steps

def take_slice(step, alpha, image, side):
    """Extract step'th slice"""

    slice = np.empty((side, 3))
    center = half = int((side-1)/2)
    slice[center] = image[center][center]
    step_alpha = step*alpha

    cos_ratio = np.cos(step_alpha)
    sin_ratio = np.sin(step_alpha)

    i, j = 0.0, 0.0
    for n in range(1, half):
        i += cos_ratio
        j += sin_ratio

        slice[center+n] = cv.getRectSubPix(image, (1,1), (center+i, center-j))
        slice[center-n] = cv.getRectSubPix(image, (1,1), (center-i, center+j))

    return slice

def virtual_real_lengths(side):
    return (int(side/3), int(side/3))

def split_slice(slice, virtual_length, real_length):
    """Splice a slice into left, central and right parts"""

    JK, LM = np.empty((virtual_length, 3)), np.empty((virtual_length, 3))
    KL = np.empty((real_length, 3))

    JK = slice[:virtual_length]
    KL = slice[virtual_length:virtual_length+real_length]
    LM = \
     slice[virtual_length+real_length:virtual_length+real_length+virtual_length]

    return (JK, KL, LM)
