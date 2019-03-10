import numpy as np
import pptk

import sys

POINT_SIZE = 0.08

def display_recovered(filename):

    points_left = np.load(filename+" left points recovered.npy")
    points_right = np.load(filename+" right points recovered.npy")

    l = pptk.viewer(points_left, points_left[:, 2])
    l.set(point_size=POINT_SIZE, lookat=(0,0,0), bg_color=np.array([0,0,0,0], np.float), show_axis=False, show_grid=False)
    r = pptk.viewer(points_right, points_right[:, 2])
    r.set(point_size=POINT_SIZE, lookat=(0,0,10), bg_color=np.array([0,0,0,0], np.float), show_axis=False, show_grid=False)

arg = sys.argv[1]
if (arg == "bread01"):
    FILENAME = "img/bread01/bread01_square resized (750, 750) (9, 9)"
    display_recovered(FILENAME)
elif (arg == "bread02"):
    FILENAME = "img/bread02/bread02_square resized (750, 750) (9, 9)"
    display_recovered(FILENAME)
else:
    print("Not valid")
