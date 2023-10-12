# Aula_02_ex_07.py
# 
# Historam visualization with openCV
#


# import
import cv2
import numpy as np

####################
# Compute Histogram
####################
def compute_histogram(image,histSize, histRange):
	# Compute the histogram
	hist_item = cv2.calcHist([image], [0], None, [histSize], histRange)
	return hist_item

##########################################
# Drawing with openCV
# Create an image to display the histogram
def histogram2image(hist_item, histSize, histImageWidth, histImageHeight, color):

	histImage = np.zeros((histImageWidth, histImageHeight, 1), np.uint8)

	# Width of each histogram bar
	binWidth = int(np.ceil(histImageWidth * 1.0 / histSize))

	# Normalize values to [0, histImageHeight]
	cv2.normalize(hist_item, hist_item, 0, histImageHeight, cv2.NORM_MINMAX)

	# Draw the bars of the nomrmalized histogram
	for i in range(histSize):
		cv2.rectangle(histImage, (i * binWidth, 0), ((i + 1) * binWidth, int(hist_item[i])), color, -1)

	# ATTENTION : Y coordinate upside down
	histImage = np.flipud(histImage)

	return histImage


# histogram variables
histSize = 256
histRange = [0, 256]
histImageWidth = 512
histImageHeight = 512
color = (125)

# Read the image
image = cv2.imread("Orchid.bmp")

# Image characteristics
height, width = image.shape[0:2]

# Show the image
cv2.imshow( "Image", image )

# Original Image Histogram
hist_item =  compute_histogram(image, histSize, histRange)
histImage =  histogram2image(hist_item, histSize, histImageWidth, histImageHeight, color)
cv2.imshow('Original Image Histogram', histImage)



image_b, image_g, image_r = cv2.split(image)

# Show the image
cv2.imshow( "Image Red", image_r )

# Original Image Histogram
hist_item =  compute_histogram(image_r, histSize, histRange)
histImage =  histogram2image(hist_item, histSize, histImageWidth, histImageHeight, color)
cv2.imshow('Image Red Histogram', histImage)

cv2.imshow( "Image Green", image_g )

# Original Image Histogram
hist_item =  compute_histogram(image_g, histSize, histRange)
histImage =  histogram2image(hist_item, histSize, histImageWidth, histImageHeight, color)
cv2.imshow('Image Green Histogram', histImage)

cv2.imshow( "Image Blue", image_b )

# Original Image Histogram
hist_item =  compute_histogram(image_b, histSize, histRange)
histImage =  histogram2image(hist_item, histSize, histImageWidth, histImageHeight, color)
cv2.imshow('Image Blue Histogram', histImage)



# Wait
cv2.waitKey()

# Destroy the window -- might be omitted
cv2.destroyWindow( "Display window" )