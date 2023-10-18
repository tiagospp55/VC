import cv2
import numpy as np


image = cv2.imread("wdg2.bmp", cv2.IMREAD_GRAYSCALE)

retval, image_threshold = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)

image_inverted = cv2.bitwise_not(image_threshold[1])

retangular_structure = np.ones((3,3), np.uint8)

image_dilatation = cv2.dilate(image_inverted, retangular_structure, iterations= 1)
image_subtracted = cv2.subtract(image_dilatation, image_inverted)

cv2.imshow("original", image)
cv2.imshow("dilatation", image_dilatation)
cv2.imshow("subtracted", image_subtracted)

#Aumentar o elemento estruturante faz com que os contornos se realcem 

cv2.waitKey(0)