

#import
import numpy as np
import cv2
import sys

def mouse_handler(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		print(x,y)
		cv2.floodFill(image, None, (x,y), 255,5,5)
		cv2.imshow( "Display Window", image )


# Read the image
image = cv2.imread( 'lena.jpg', cv2.IMREAD_UNCHANGED )




if  np.shape(image) == ():
	# Failed Reading
	print("Image file could not be open")
	exit(-1)

# Image characteristics
height, width = image.shape

print("Image Size: (%d,%d)" % (height, width))
print("Image Type: %s" % (image.dtype))



cv2.namedWindow( "Display Window", cv2.WINDOW_AUTOSIZE )
cv2.setMouseCallback("Display Window", mouse_handler)

# Show the image
cv2.imshow( "Display Window", image )

# Wait
cv2.waitKey( 0 )

# Destroy the window -- might be omitted
cv2.destroyWindow( "Display Window" )
