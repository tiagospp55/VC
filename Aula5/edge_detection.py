import argparse
import cv2
import numpy as np

def main():
  

    image = cv2.imread('wdg2.bmp', cv2.IMREAD_GRAYSCALE) # Load an image 

    #converting to binary with threshold of 120
    retval, img_thresholded = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)

    #inverting image
    image = cv2.bitwise_not(img_thresholded)

    #square structuring point structuring point
    square_struct_point_3x3 = np.ones((3,3), np.uint8)
    square_struct_point_7x7 = np.ones((7,7), np.uint8)


    square_img_dilation_3x3 = cv2.dilate(image, square_struct_point_3x3, iterations=1)
    square_img_dilation_7x7 = cv2.dilate(image, square_struct_point_7x7, iterations=1)

    edges_3x3=cv2.subtract(square_img_dilation_3x3, image)
    edges_7x7=cv2.subtract(square_img_dilation_7x7, image)
    


    cv2.imshow('original', image)
    cv2.imshow('edges 3x3', edges_3x3)
    cv2.imshow('edges 7x7', edges_7x7)


    cv2.waitKey(0)

if __name__ == "__main__":
    main()