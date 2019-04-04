import numpy as np
import cv2 as cv

from matplotlib import pyplot as plt
from src.load_save import load_image, save_image

#use normalized cross-correlation as comparison method
METHOD = cv.TM_CCORR_NORMED

def stereo_matching(filename, ext, window_shape, bound):
    """save disparity maps and correspondance maps between
       left-central and central-right images"""

    print("stereo matching " + filename)

    left_image, central_image, right_image = \
                                       (load_image(filename+" left", ext),
                                        load_image(filename+" central", ext),
                                        load_image(filename+" right", ext))

    H, W, _ = central_image.shape
    h, w = window_shape

    filename += (" "+str(window_shape))

    disparity_map_left, correspondance_left = \
              template_matching_cl(central_image, left_image, H, W, h, w, bound)
    np.save(filename+" disparity map left", disparity_map_left)
    np.save(filename+" correspondance left", correspondance_left)

    disparity_map_right, correspondance_right = \
             template_matching_cr(central_image, right_image, H, W, h, w, bound)
    np.save(filename+" disparity map right", disparity_map_right)
    np.save(filename+" correspondance right", correspondance_right)

    print("end stereo matching " + filename)

def template_matching_cl(central_image, left_image, H, W, h, w, bound):
    """compute disparity map and correspondance map between
       left-central. Maps values are bounded by bound"""

    disparity_map = np.empty((H-h+1, W-w+1))
    correspondance = np.empty((H-h+1, W-w+1))

    for y in range(0, H-h+1):
        for x in range(0, W-w+1):
            lower_bound = np.max((0, x-bound))
            upper_bound = np.max((0, x+1))

            horizontal_slice = left_image[y:y+h, lower_bound:upper_bound]

            template = central_image[y:y+h, x:x+w]

            result = cv.matchTemplate(template, horizontal_slice, METHOD)

            _, _, _, max_location = cv.minMaxLoc(result)

            disparity = -(upper_bound-lower_bound - max_location[0])

            disparity_map[y, x] = disparity
            correspondance[y, x] = x+disparity

    return (disparity_map, correspondance)

def template_matching_cr(central_image, right_image, H, W, h, w, bound):
    """compute disparity map and correspondance map between
       cemtral-right. Maps values are bounded by bound"""

    disparity_map = np.empty((H-h+1, W-w+1))
    correspondance = np.empty((H-h+1, W-w+1))

    for y in range(0, H-h+1):
        for x in range(0, W-w+1):
            lower_bound = np.min((x, W-w+1))
            upper_bound = np.min((x+bound, W-w+1))

            horizontal_slice = right_image[y:y+h, lower_bound:upper_bound]

            template = central_image[y:y+h, x:x+w]

            result = cv.matchTemplate(horizontal_slice, template, METHOD)

            _, _, _, max_location = cv.minMaxLoc(result)

            disparity_map[y, x] = max_location[0]
            correspondance[y, x] = x+max_location[0]

    return (disparity_map, correspondance)
