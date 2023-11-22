# Aula_05_exe_01.py
#
# Cube Inprinting in Video Capture
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

distortion = np.array([])
intrinsics = []


with np.load('camera_params.npz') as data: 
    intrinsics = data['intrinsics'] 
    distortion = data['distortion']

cameraMatrix = np.array([[intrinsics[0], 0, intrinsics[2]], [0, intrinsics[1], intrinsics[3]], [0,0,1]])

capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()

    k = cv2.waitKey(1)

    if k == ord("q"): 
        break
        
    ret, corners = FindAndDisplayChessboard(frame)

    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        #ret, cam, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame.shape[:2], 0, 0)
        #determinate the orientation and position of the object 
        retval, rvec, tvec = cv2.solvePnP(objpoints[-1], imgpoints[-1], cameraMatrix, distortion)

        retval, _ = cv2.projectPoints(np.float64([[0,0,0],[0,0,-2],[0,2,0],[2,0,0], [2,2,-2], [2,2,0], [2,0,-2], [0,2,-2]]), rvec, tvec, cameraMatrix, distortion)

       
        # vertical lines
        cv2.line(frame, (int(retval[0][0][0]), int(retval[0][0][1])), (int(retval[1][0][0]), int(retval[1][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[2][0][0]), int(retval[2][0][1])), (int(retval[7][0][0]), int(retval[7][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[5][0][0]), int(retval[5][0][1])), (int(retval[4][0][0]), int(retval[4][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[3][0][0]), int(retval[3][0][1])), (int(retval[6][0][0]), int(retval[6][0][1])), (0,0,255), 3)

        # first rectangle lines
        cv2.line(frame, (int(retval[0][0][0]), int(retval[0][0][1])), (int(retval[2][0][0]), int(retval[2][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[0][0][0]), int(retval[0][0][1])), (int(retval[3][0][0]), int(retval[3][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[5][0][0]), int(retval[5][0][1])), (int(retval[2][0][0]), int(retval[2][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[5][0][0]), int(retval[5][0][1])), (int(retval[3][0][0]), int(retval[3][0][1])), (0,0,255), 3)

        # second rectangle lines
        cv2.line(frame, (int(retval[1][0][0]), int(retval[1][0][1])), (int(retval[7][0][0]), int(retval[7][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[1][0][0]), int(retval[1][0][1])), (int(retval[6][0][0]), int(retval[6][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[4][0][0]), int(retval[4][0][1])), (int(retval[7][0][0]), int(retval[7][0][1])), (0,0,255), 3)
        cv2.line(frame, (int(retval[4][0][0]), int(retval[4][0][1])), (int(retval[6][0][0]), int(retval[6][0][1])), (0,0,255), 3)

        # rectangles
        # cv2.rectangle(frame, (int(retval[2][0][0]), int(retval[2][0][1])), (int(retval[3][0][0]), int(retval[3][0][1])), (0,0,255), 3)
        # cv2.rectangle(frame, (int(retval[7][0][0]), int(retval[7][0][1])), (int(retval[6][0][0]), int(retval[6][0][1])), (0,0,255), 3)

    cv2.imshow('video', frame)

#cv2.imshow('img',img)
cv2.waitKey(-1)
cv2.destroyAllWindows()