 # Cheesboard.py
 #
 # Chessboard Calibration
 #
 # Paulo Dias

import numpy as np
import cv2
import glob

# Board Size
board_h = 9
board_w = 6




def  FindAndDisplayChessboard(img):
    # Find the chess board corners
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(img, (board_w,board_h),None)

    # If found, display image with corners
    if ret == True:
        img = cv2.drawChessboardCorners(img, (board_w, board_h), corners, ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

    return ret, corners

criteria = (cv2.TermCriteria_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30 , 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((board_w*board_h,3), np.float32)
objp[:,:2] = np.mgrid[0:board_w,0:board_h].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
imgpointsR = [] # 2d points in image plane.

# Read images
imagesLeft = sorted(glob.glob('images/left*.jpg'))
imagesRight = sorted(glob.glob('images/right*.jpg'))

for imgLeft,imgRight, in zip(imagesLeft, imagesRight):
    imgL = cv2.imread(imgLeft)
    imgR = cv2.imread(imgRight)

    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    retL, cornersL = FindAndDisplayChessboard(grayL)
    retR,cornersR  = FindAndDisplayChessboard(grayR)
    if retL and retR == True:
        objpoints.append(objp)
        
        cornorsL = cv2.cornerSubPix(grayL, cornersL, (11,11),(-1,-1), criteria)
        imgpointsL.append(cornorsL)

        cornorsR = cv2.cornerSubPix(grayR, cornersR, (11,11),(-1,-1), criteria)
        imgpointsR.append(cornorsR)

        cv2.drawChessboardCorners(imgL,(board_w,board_h), cornersL, retL)
        cv2.imshow('img Left', imgL)

        cv2.drawChessboardCorners(imgR,(board_w,board_h), cornersR, retR)
        cv2.imshow('img Right', imgR)
        cv2.waitKey(500)



retL, cameraMatrixL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL,(board_w,board_h), None, None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL,heightL), 1 , (widthL,heightL))

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR,(board_w,board_h), None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv2.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR,heightR), 1 , (widthR,heightR))

flags =0
flags |= cv2.CALIB_FIX_INTRINSIC


criteria_stereo=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(objpoints, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, cv2.CALIB_USE_INTRINSIC_GUESS)

np.savez("stereoParams.npz", 
         intrinsics1=newCameraMatrixL, 
         distortion1=distL, 
         intrinsics2=newCameraMatrixR,
         distortion2=distR, 
         R=rot, T=trans, E=essentialMatrix, F=fundamentalMatrix)

img1=cv2.imread('left05.jpg')
img2=cv2.imread('right05.jpg')


# undist1 = cv2.undistort(img1,cameraMatrixL, distL, None, newCameraMatrixL)
# undist2 = cv2.undistort(img2,cameraMatrixR, distR, None, newCameraMatrixR)

# cv2.imshow('img1',undist1)
# cv2.imshow('img2',undist2)
cv2.imshow('img1_original',img1)
cv2.imshow('img2_original',img2)


cv2.waitKey(-1)
cv2.destroyAllWindows()