 # Aula_01_ex_01.py
 #
 # Cheesboard Calibration
 #
 # Paulo Dias

import numpy as np
import cv2
import glob

# Board Size
board_h = 9
board_w = 6

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


def  FindAndDisplayChessboard(img):
    # Find the chess board corners
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (board_w,board_h),None)

    # If found, display image with corners
    if ret == True:
         img = cv2.drawChessboardCorners(img, (board_w, board_h), corners, ret)
   
   
   
    #     cv2.imshow('img',img)
    #     cv2.waitKey(500)

    return ret, corners


capture = cv2.VideoCapture(0)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((board_w*board_h,3), np.float32)
objp[:,:2] = np.mgrid[0:board_w,0:board_h].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Read images
images = sorted(glob.glob('images/left*.jpg'))

for fname in images:
    img = cv2.imread(fname)
    ret, corners = FindAndDisplayChessboard(img)
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)


height, width, channels = img.shape
s = (width, height)
print(s)

rev, intrinsics, distortion, rvecs, tvecs =  cv2.calibrateCamera(objpoints, imgpoints,(width, height), None, None)

print("Intrinsics: ")
print (intrinsics)
print("Distortion : ")
print(distortion)
for i in range(len(tvecs)):
    print ("Translations(%d) : " % i )
    print(tvecs[0])
    print ("Rotation(%d) : " % i )
    print(rvecs[0])


np.savez('camera.npz', intrinsics = intrinsics, distorcion = distortion)

nload = np.load('camera.npz')

#Read and display line,
fname = images[0]
img = cv2.imread(fname)

# axis = np.float32([[0,0,0],[3,0,0],[0,3,0],[0,0,-3]]).reshape(-1,3)
# imgpoints, jac = cv2.projectPoints(axis, rvecs[0], tvecs[0], intrinsics, distortion)
# img = cv2.line(img, np.int32(imgpoints[0].ravel()), np.int32(imgpoints[1].ravel()), (255,0,0),5)
# img = cv2.line(img, np.int32(imgpoints[0].ravel()), np.int32(imgpoints[2].ravel()), (0,255,0),5)
# img = cv2.line(img, np.int32(imgpoints[0].ravel()), np.int32(imgpoints[3].ravel()), (0,0,255),5)

axis = np.float32([[0,0,0],[3,0,0],[0,3,0],[0,0,-3]]).reshape(-1,3)
for x in range(0,len(images)):
    print(x)
    fname = images[x]
    img = cv2.imread(fname)
    imgpoints, jac = cv2.projectPoints(axis, rvecs[x], tvecs[x], intrinsics, distortion)
    img = cv2.line(img, np.int32(imgpoints[0].ravel()), np.int32(imgpoints[1].ravel()), (255,0,0),5)
    img = cv2.line(img, np.int32(imgpoints[0].ravel()), np.int32(imgpoints[2].ravel()), (0,255,0),5)
    img = cv2.line(img, np.int32(imgpoints[0].ravel()), np.int32(imgpoints[3].ravel()), (0,0,255),5)
    cv2.imshow('img',img)
    cv2.waitKey()

cv2.waitKey(-1)
cv2.destroyAllWindows()