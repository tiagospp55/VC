# Aula_06_exe_02.py
#
# Stereo Chessboard Calibration
#
# Filipe Gonçalves - 11/2022

import numpy as np
import cv2
import glob

# Board Size
board_h = 9
board_w = 6

def FindAndDisplayChessboard(img):
    # Find the chess board corners
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (board_w,board_h),None)

    # If found, display image with corners
    if ret == True:
        img = cv2.drawChessboardCorners(img, (board_w, board_h), corners, ret)

    return ret, corners

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((board_w*board_h,3), np.float32)
objp[:,:2] = np.mgrid[0:board_w,0:board_h].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
left_corners = [] # 2d points in image plane.
right_corners = [] # 2d points in image plane.

# Read images
images_l = sorted(glob.glob('.//images//left*.jpg'))
images_r = sorted(glob.glob('.//images//right*.jpg'))

for fname_l, fname_r in zip(images_l, images_r):
    img_l = cv2.imread(fname_l)
    img_r = cv2.imread(fname_r)
    ret1, l_corners = FindAndDisplayChessboard(img_l)
    ret2, r_corners = FindAndDisplayChessboard(img_r)
    if ret1 and ret2:
        objpoints.append(objp)
        left_corners.append(l_corners)
        right_corners.append(r_corners)     

# stereo calibration
retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints, left_corners, right_corners, 0,0,0,0, img_l.shape[:2], flags=cv2.CALIB_SAME_FOCAL_LENGTH)

np.savez("stereoParams.npz", 
         intrinsics1=cameraMatrix1, 
         distortion1=distCoeffs1, 
         intrinsics2=cameraMatrix2, 
         distortion2=distCoeffs2, 
         R=R, T=T, E=E, F=F)