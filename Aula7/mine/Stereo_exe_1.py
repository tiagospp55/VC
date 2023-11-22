# ***********************************************************************************
# Name:           chessboard.py
# Revision:
# Date:           28-10-2019
# Author:         Paulo Dias
# Comments:       ChessBoard Tracking
#
# images         left1.jpg->left19.jpg
# Revision:
# ***********************************************************************************
import numpy as np
import cv2
import glob

# Board Size
board_h = 9
board_w = 6

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints_left = [] # 2d points in image plane.
imgpoints_right = [] # 2d points in image plane.


def  FindAndDisplayChessboard(img):
    # Find the chess board corners
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (board_w,board_h),None)

    # If found, display image with corners
    if ret == True:
        img = cv2.drawChessboardCorners(img, (board_w, board_h), corners, ret)
        cv2.imshow('img',img)
        cv2.waitKey(100)

    return ret, corners

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((board_w*board_h,3), np.float32)
objp[:,:2] = np.mgrid[0:board_w,0:board_h].T.reshape(-1,2)

# Read images
left_images = sorted(glob.glob('images/left*.jpg'))
right_images = sorted(glob.glob('images/right*.jpg'))

dimensions=None

for image in right_images:
    img = cv2.imread(image)
    ret, corners = FindAndDisplayChessboard(img)
    if ret == True:
        objpoints.append(objp)
        imgpoints_right.append(corners)


for image in left_images:
    dimensions=img.shape[:2]
    img = cv2.imread(image)
    ret, corners = FindAndDisplayChessboard(img)
    if ret == True:
        imgpoints_left.append(corners)

#dimensions.reverse()

#Calibração stereo
ret, mtx_left, dist_left, mtx_right, dist_right, R, T,E, F = cv2.stereoCalibrate(
    objpoints, imgpoints_left, imgpoints_right, 
    None, None, None, None, dimensions, 
    flags=cv2.CALIB_SAME_FOCAL_LENGTH)

np.savez("stereoParams.npz", 
        intrinsics1 = mtx_left, distortion1 = dist_left, 
        intrinsics2 = mtx_right, distortion2 = dist_right, 
        R=R, T=T, E=E, F=F)

cv2.waitKey(-1)
cv2.destroyAllWindows()