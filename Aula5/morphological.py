import cv2 

image = cv2.imread("mon1.bmp", cv2.IMREAD_GRAYSCALE)
retval ,image_threshold = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)

circular_struct_point=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))

image_erosion = cv2.erode(image_threshold, circular_struct_point, iterations=2)

cv2.imshow("original", image)
cv2.imshow("Threshold", image_threshold)
cv2.imshow("erosion", image_erosion)

cv2.waitKey(0)

# A PARTE NEGRA VAI AUMENTANDO