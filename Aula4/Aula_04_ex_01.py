

import cv2 as cv
import numpy as np



image = cv.imread( "lena.jpg", cv.IMREAD_GRAYSCALE )

if  np.shape(image) == ():
    # Failed Reading
    print("Image file could not be open!")
    exit(-1)

cv.imshow('Orginal', image)

retval, image2 = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
cv.imshow('Binary', image2)

retval, image3 = cv.threshold(image, 127, 255, cv.THRESH_BINARY_INV)
cv.imshow('Binary Inv', image3)

retval, image4 = cv.threshold(image, 127, 255, cv.THRESH_TRUNC)
cv.imshow('Trunc', image4)

retval, image5 = cv.threshold(image, 127, 255, cv.THRESH_TOZERO)
cv.imshow('To Zero', image5)

retval, image6 = cv.threshold(image, 127, 255, cv.THRESH_TOZERO_INV)
cv.imshow('To Zero Inv', image6)

cv.waitKey(0)