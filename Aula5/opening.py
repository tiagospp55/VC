import cv2 
import numpy as np
image = cv2.imread("art4.bmp", cv2.IMREAD_GRAYSCALE)
retval ,image_threshold = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)

circular_struct_point=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))

image_erosion = cv2.erode(image_threshold, circular_struct_point, iterations=5)

mage = cv2.bitwise_not(image_erosion)

#circular Structuring 
circular_struct_point=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))

#square structuring point structuring point
square_struct_point = np.ones((22,22), np.uint8)

circular_img_dilation = cv2.dilate(image, circular_struct_point, iterations=1)

cv2.imshow("original", image)
cv2.imshow("Threshold", image_threshold)
cv2.imshow("erosion", image_erosion)
cv2.imshow("inverted", mage)
cv2.imshow("dilation", circular_img_dilation)


cv2.waitKey(0)  