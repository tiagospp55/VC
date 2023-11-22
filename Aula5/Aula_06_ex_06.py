
#Aula 5 ex 06
import cv2 
import numpy as np 

image = cv2.imread( "art4.bmp", cv2.IMREAD_GRAYSCALE );
  

kernel =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10));
kernel1 =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(22,22));
kernel2 =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(35,35));

#Dilate and then erode 
img_dilation = cv2.dilate(image, kernel, iterations=1) 
img_erosion = cv2.erode(img_dilation, kernel, iterations=1) 
img_dilation1 = cv2.dilate(image, kernel1, iterations=1) 
img_erosion1 = cv2.erode(img_dilation1, kernel1, iterations=1) 
img_dilation2 = cv2.dilate(image, kernel2, iterations=1) 
img_erosion2 = cv2.erode(img_dilation2, kernel2, iterations=1) 

  
cv2.imshow('Input', image) 
cv2.imshow('Dilation', img_dilation) 
cv2.imshow('Erosion', img_erosion) 


cv2.imshow('Dilation1', img_dilation1) 
cv2.imshow('Erosion1', img_erosion1) 


cv2.imshow('Dilation2', img_dilation2) 
cv2.imshow('Erosion2', img_erosion2) 


cv2.waitKey(0)
