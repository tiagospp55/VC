# Aula_02_ex_05.py
# 
# Historam visualization with openCV
#

# Que imagem é suposto usar?

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
image = cv2.imread( "images/input.png", cv2.IMREAD_UNCHANGED );

# Image characteristics
height, width = image.shape[0:2]

if len(image.shape) == 3:
    # Turn image into gray scale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create a vsiualization window (optional)
# CV_WINDOW_AUTOSIZE : window size will depend on image size
cv2.namedWindow( "Contrast Stretchng", cv2.WINDOW_AUTOSIZE )

# # Show the image
cv2.imshow( "Original", image )

# Original Image Histogram
hist_item =  compute_histogram(image, histSize, histRange)
histImage =  histogram2image(hist_item, histSize, histImageWidth, histImageHeight, color)
cv2.imshow('Original Image Histogram', histImage)

# Contrast Stretching
minL, maxL, minP, maxP = cv2.minMaxLoc(image)

contrast_image = image.copy()

for x in range(height):
    for y in range(width):
        contrast_image[x][y] = int(((image[x][y] - minL) / (maxL - minL)) * 255)


cv2.imshow( "Contrast Stretchng", contrast_image )

# Contrast Image Histogram
hist_item = compute_histogram(contrast_image.astype(np.float32), histSize, histRange)
histImage = histogram2image(hist_item, histSize, histImageWidth, histImageHeight, color)
cv2.imshow('Contrast Stretchng Histogram', histImage)

# Wait
cv2.waitKey()

# Destroy the window -- might be omitted
cv2.destroyWindow( "Display window" )