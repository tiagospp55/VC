 # reconstruction.py
 #
 # Example for 3D reconstruction
 #
 # Paulo Dias

import numpy as np
import cv2
import glob


# Mouse handler
def mouse_handler_l(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # random color
        color = np.random.randint(0, 255, 3).tolist()
        # Draw line
        image = params
        cv2.line(image, (0, int(y)), (width, int(y)), color, 4)
        cv2.imshow("Right", image);
        cv2.waitKey(1)

def mouse_handler_r(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # random color
        color = np.random.randint(0, 255, 3).tolist()
        # Draw line
        image = params
        cv2.line(image, (0, int(y)), (width, int(y)), color, 4)
        cv2.imshow("Left", image);
        cv2.waitKey(1)

# Load camera parameters
with np.load('stereoParams.npz') as data:
    intrinsics1 = data['intrinsics1']
    distortion1 = data['distortion1']
    intrinsics2 = data['intrinsics2']
    distortion2 = data['distortion2']
    R = data['R']
    T = data['T']
    E = data['E']
    F = data['F']

# Reading image
left = cv2.imread('images/left02.jpg')
undistort_left = cv2.undistort(left, intrinsics1, distortion1)

right = cv2.imread('images/right02.jpg')
undistort_right = cv2.undistort(right, intrinsics2, distortion2)

# stereo rectification
print("StereoRectifyMap");
height, width, depth =  undistort_left.shape

#R1,T1,R2,T2,Q = cv2.stereoRectify(intrinsics1, distortion1, intrinsics2, distortion2, (width,height), R, T, 0);
R1 = np.zeros(shape=(3,3))
R2 = np.zeros(shape=(3,3))
P1 = np.zeros(shape=(3,4))
P2 = np.zeros(shape=(3,4))
Q = np.zeros(shape=(4,4))

cv2.stereoRectify(intrinsics1, distortion1, intrinsics2, distortion2 ,(width, height), R, T, R1, R2, P1, P2, Q, flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1, newImageSize=(0,0))

# Map computation
print("InitUndistortRectifyMap")
map1x, map1y = cv2.initUndistortRectifyMap(intrinsics1, distortion1, R1, P1, (width,height), cv2.CV_32FC1)
map2x, map2y = cv2.initUndistortRectifyMap(intrinsics2, distortion2, R2, P2, (width,height), cv2.CV_32FC1)

# Image Remaping
print("Remap images")
remap_imgl = None
gray_imagel = cv2.cvtColor(undistort_left, cv2.COLOR_BGR2GRAY)
remap_imgl = cv2.remap(gray_imagel, map1x, map1y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)

remap_imgr = None
gray_imager = cv2.cvtColor(undistort_right, cv2.COLOR_BGR2GRAY)
remap_imgr = cv2.remap(gray_imager, map2x, map2y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)



# Call the constructor for StereoBM
stereo = cv2.StereoSGBM_create(numDisparities =16*5 , blockSize =21)

# Calculate the disparity image
disparity = stereo.compute(remap_imgl, remap_imgr)


# -- Display as a CV_8UC1 image
disparity = cv2.normalize(src=disparity, dst=disparity, beta=0, alpha=255,
norm_type=cv2.NORM_MINMAX)
disparity = np.uint8(disparity)



depth = cv2.reprojectImageTo3D(disparity, Q)



cv2.imshow("left", left)
cv2.imshow("right", right)
cv2.imshow('Disparity Map', disparity)
cv2.waitKey()

np.savez('3DCoordinates.npz', depth = depth, disparity = disparity, Q = Q)


cv2.destroyAllWindows()