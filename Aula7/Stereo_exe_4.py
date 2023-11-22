

import numpy as np
import cv2
import glob
from functools import partial

def mouse_handler(event, x, y, flags, params, img, window_name):

    if event == cv2.EVENT_LBUTTONDOWN:
        p = np.asarray([x,y]) 
        epilineR = cv2.computeCorrespondEpilines(p.reshape(-1,1,2), 1, F) 
        epilineR = epilineR.reshape(-1,3)[0]
        color = np.random.randint(0, 255, 3).tolist()

        points_x = [0, img.shape[1]]
        m = - epilineR[0]/epilineR[1]
        b = - epilineR[2]/epilineR[1]

        points = [  (points_x[0], int(m*points_x[0]+b)), 
                    (points_x[1], int(m*points_x[1]+b))   ]

        cv2.line(img, points[0], points[1], color, 2)
        cv2.imshow(window_name, img)

with np.load('stereoParams.npz') as data: 
    intrinsics1 = data['intrinsics1'] 
    distortion1 = data['distortion1']
    intrinsics2 = data['intrinsics2'] 
    distortion2 = data['distortion2']
    R = data['R']
    T = data['T']
    E = data['E']
    F = data['F']
    
# Read images
images_l = sorted(glob.glob('.//images//left*.jpg'))
images_r = sorted(glob.glob('.//images//right*.jpg'))

img_l = cv2.imread(images_l[1])
img_r = cv2.imread(images_r[1])

img_undistort_l = cv2.undistort(img_l, intrinsics1, distortion1)
img_undistort_r = cv2.undistort(img_r, intrinsics2, distortion2)

cv2.imshow("Left Undistort", img_undistort_l)
cv2.imshow("Right Undistort", img_undistort_r)


cv2.setMouseCallback("Left Undistort", partial(mouse_handler, img=img_undistort_r, window_name="Right Undistort"))
cv2.setMouseCallback("Right Undistort", partial(mouse_handler, img=img_undistort_l, window_name="Left Undistort"))

cv2.waitKey(-1)
cv2.destroyAllWindows()