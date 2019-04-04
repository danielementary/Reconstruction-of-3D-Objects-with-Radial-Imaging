import numpy as np
import cv2 as cv

def recover_shape(filename, views_shape):
    """Rotate horizontal slices of reconstructed points to recover the initial
       disk shape"""

    print("recover shape "+filename)
    helper(filename+" left points", views_shape)
    helper(filename+" right points", views_shape)
    print("end recover shape"+filename)


def helper(filename, views_shape):

    points = np.load(filename+".npy")
    steps = views_shape[0]

    #degrees per steps
    alpha = np.pi/steps

    recovered = []

    angle = 0
    counter = 0
    for p in points.T:
        p = p[0]
        x, y, z = p
        s, c = np.sin(angle), np.cos(angle)

        #store the new coordinates rotated around the z-axis depending on angle
        recovered.append([x*c, x*s, z])
        counter += 1
        angle += alpha

    recovered_np = np.array(recovered)

    np.save(filename+" recovered.npy", recovered_np)
