import numpy as np
import cv2 as cv

def load_image(filename, ext, format=cv.IMREAD_COLOR):
    temp = cv.imread(filename+ext, format)

    if temp is not None:
        return temp
    else:
        print("impossible to read " + filename+ext)

def save_image(filename, ext, image):
    cv.imwrite(filename+ext, image)
    print("saved image " + filename+ext)

def save_three_views(filename, ext, left_view, central_view, right_view):
    cv.imwrite(filename + " left" + ext, left_view)
    cv.imwrite(filename + " central" + ext, central_view)
    cv.imwrite(filename + " right" + ext, right_view)

    print("3 saved images " + filename)

def save_merged_views(filename, ext, left_view, central_view, right_view):
    h1, h2, h3 = (left_view.shape[0], central_view.shape[0], \
                  right_view.shape[0])

    if (h1 != h2 or h2 != h3):
        print("Images cannot be merged")
        return

    vertical_line = np.full((h1, 5, 3), 255)

    temp = np.concatenate((left_view, vertical_line, \
                           central_view, vertical_line, \
                           right_view), axis=1)

    cv.imwrite(filename + " merged" + ext, temp)

    print("saved merged images "+filename)
