import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys


image = cv2.imread( sys.argv[1], cv2.IMREAD_UNCHANGED );



if  np.shape(image) == ():

	print("Image file could not be open")
	exit(-1)


height, weight = image.shape[0:2]

size = 20

image_grid = np.copy(image)

if len(image.shape) < 3:
    for x in range(0, weight, size):
        cv2.line(image_grid, (x, 0), (x, height), (255,255,255), 1)

    for y in range(0, height, size):
        cv2.line(image_grid, (0, y), (weight, y), (255,255,255), 1)
    cv2.imwrite("image_grid_grey.jpg", image_grid)
elif len(image.shape) >= 3:
    for x in range(0, weight, size):
        cv2.line(image_grid, (x, 0), (x, height), (0, 0, 0), 1)

    for y in range(0, height, size):
        cv2.line(image_grid, (0, y), (weight, y), (20, 20, 20), 1)
    cv2.imwrite("image_grid_rgb.jpg", image_grid)
image_grid_rgb = cv2.cvtColor(image_grid, cv2.COLOR_BGR2RGB)



plt.imshow(image_grid_rgb)
plt.show()