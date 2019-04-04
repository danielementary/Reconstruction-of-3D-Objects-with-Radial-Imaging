import numpy as np
import cv2 as cv

from src.load_save import load_image, save_image

#mathematical functions

def csc(alpha):
    return 1.0/np.sin(alpha)

def cot(alpha):
    return np.cos(alpha)/np.sin(alpha)

#function to compute project specific parameters

def angle_of_view(dimension, focal_length):
    return 2*np.arctan2(dimension, 2.0*focal_length)

def distance_focal_length(angle_of_view, dimension):
    return dimension/(2.0*np.tan(angle_of_view/2.0))

def distance_d(radius, theta):
    return radius*cot(theta)

def distance_vr(radius):
    return 2.0*radius

def distance_vd(radius, theta):
    return 0.0

def maximum_length(radius, theta):
    return 2.0*radius*np.cos(theta)*csc(theta)

def virtual_FOV(theta):
    return np.arctan2(2.0*np.cos(theta)*np.sin(theta)*np.sin(theta), \
                    np.sin(theta)+2.0*np.sin(theta)*np.cos(theta)*np.cos(theta))

def real_FOV(theta):
    return 2.0*(theta-virtual_FOV(theta))

def angle_delta(theta):
    return (theta-0.5*virtual_FOV(theta))

def resize(filename, ext, dimensions):

    print("image resize " + filename)

    img = load_image(filename, ext)
    img = cv.resize(img, dimensions)

    save_image(filename+" resized "+str(dimensions), ext, img)

    print("end image resize " + filename)

def from_homogeneous_to_cartesian(point):
    return point[:-1]/point[-1]
