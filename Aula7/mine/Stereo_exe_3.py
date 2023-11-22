import cv2
import numpy as np

with np.load('stereoParams.npz') as params:
    intrinsics_left= params["intrinsics1"]
    distortion_left=params["distortion1"]
    intrinsics_right= params["intrinsics2"]
    distortion_right=params["distortion2"]
    R= params["R"]
    T=params["T"]
    E= params["E"]
    F=params["F"]

left_image = cv2.imread('images/left01.jpg')
right_image = cv2.imread('images/right01.jpg')

left_image_undistorted=cv2.undistort(left_image, intrinsics_left, distortion_left, None)
right_image_undistorted=cv2.undistort(right_image, intrinsics_right, distortion_right, None)


cv2.imshow("distorted left", left_image)
cv2.imshow("undistorted left", left_image_undistorted)
cv2.imshow("distorted right", right_image)
cv2.imshow("undistorted right", right_image_undistorted)

cv2.waitKey(0)
cv2.destroyAllWindows()