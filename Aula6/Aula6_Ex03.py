# Aula_05_exe_03.py
#
# Camera Calibration 
#
# Filipe Gonçalves - 11/2022

import numpy as np
import cv2
import glob

# Board Size
board_h = 9
board_w = 6

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


def FindAndDisplayChessboard(img):
    # Find the chess board corners
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (board_w,board_h),None)

    return ret, corners

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((board_w*board_h,3), np.float32)
objp[:,:2] = np.mgrid[0:board_w,0:board_h].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Read images
images = glob.glob('./chessboard.jpg')

cameraMatrix = np.array([])
distortion = np.array([])
rvecs = []
tvecs = []
intrinsics = []

capture = cv2.VideoCapture(0)

calibrated = False
count = 1

while True:
    ret, frame = capture.read()

    cv2.imshow('video', frame)

    k = cv2.waitKey(1)

    if k == ord("q"): 
        break

    if not calibrated:
        if k != -1:
        
            ret, corners = FindAndDisplayChessboard(frame)

            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

                print("Calibrating camera...")
                retval, cameraMatrix, distortion, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame.shape[:2], 0, 0)
                
                intrinsics = [cameraMatrix[0][0], cameraMatrix[1][1], cameraMatrix[0][2], cameraMatrix[1][2]]
                print(f"\t Image {count} calibrated")
                count += 1

                if count > 10:
                    calibrated = True
                    print("Calibration ended!!")
                    print("Saving file to camera_params.npz")
                    np.savez('camera_params.npz', intrinsics=intrinsics, distortion=distortion)
                    break

capture.release() 
cv2.waitKey(-1)
cv2.destroyAllWindows()