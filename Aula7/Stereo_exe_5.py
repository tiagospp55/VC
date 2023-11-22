import cv2
import numpy as np
from functools import partial

def onMouse(event, x, y, flags, params, remapped_right, remapped_left ,width, F):
    if event==cv2.EVENT_LBUTTONDOWN:
        color = np.random.randint(0,255,3).tolist()
        cv2.line(remapped_right, (0, y), (width, y), color, 1)
        cv2.line(remapped_left, (0, y), (width, y), color, 1)

        cv2.imshow("remapped right", remapped_right)
        cv2.imshow("remapped left", remapped_left)
        

def main():
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

    h,w=left_image.shape[:2]
    dimensions=(w,h)

    left_image_undistorted=cv2.undistort(left_image, intrinsics_left, distortion_left, None)
    right_image_undistorted=cv2.undistort(right_image, intrinsics_right, distortion_right, None)

   
    R1=np.zeros(shape=(3,3))
    R2=np.zeros(shape=(3,3))
    P1=np.zeros(shape=(3,4))
    P2=np.zeros(shape=(3,4))
    Q=np.zeros(shape=(4,4))

    cv2.stereoRectify(intrinsics_left, distortion_left,
                     intrinsics_right, distortion_right, 
                     dimensions, R, T, R1, R2, P1, P2, Q, 
                     flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1, newImageSize=(0,0))

    map_left_x, map_left_y=cv2.initUndistortRectifyMap(intrinsics_left, distortion_left,
                                                         R1, P1, dimensions, cv2.CV_32FC1) 

    map_right_x, map_right_y=cv2.initUndistortRectifyMap(intrinsics_right, distortion_right, R2, P2, dimensions, cv2.CV_32FC1) 

    remapped_left=cv2.remap(left_image_undistorted, map_left_x, map_left_y, cv2.INTER_LINEAR)

    remapped_right=cv2.remap(right_image_undistorted, map_right_x, map_right_y, cv2.INTER_LINEAR)


    cv2.imshow("remapped left", remapped_left)
    cv2.imshow("undistorted left", left_image_undistorted)
    cv2.imshow("undistorted right", right_image_undistorted)
    cv2.imshow("remapped right", remapped_right)

    cv2.setMouseCallback("remapped left", partial(onMouse, remapped_right=remapped_right,remapped_left=remapped_left, width=w, F=F))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()