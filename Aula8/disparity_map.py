import cv2
import numpy as np
from functools import partial   
import open3d as o3d   
        
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

    left_image_gray=cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    right_image_gray=cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)


    h,w=left_image.shape[:2]
    dimensions=(w,h)

    left_image_undistorted=cv2.undistort(left_image_gray, intrinsics_left, distortion_left, None)
    right_image_undistorted=cv2.undistort(right_image_gray, intrinsics_right, distortion_right, None)

   
    R1=np.zeros(shape=(3,3))
    R2=np.zeros(shape=(3,3))
    P1=np.zeros(shape=(3,4))
    P2=np.zeros(shape=(3,4))
    Q=np.zeros(shape=(4,4))

    cv2.stereoRectify(intrinsics_left, distortion_left, intrinsics_right, distortion_right, dimensions, R, T, R1, R2, P1, P2, Q ,flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1, newImageSize=(0,0))

    map_left_x, map_left_y=cv2.initUndistortRectifyMap(intrinsics_left, distortion_left, R1, P1, dimensions, cv2.CV_32FC1) 
    map_right_x, map_right_y=cv2.initUndistortRectifyMap(intrinsics_right, distortion_right, R2, P2, dimensions, cv2.CV_32FC1) 

    remapped_left=cv2.remap(left_image_undistorted, map_left_x, map_left_y, cv2.INTER_LINEAR)
    remapped_right=cv2.remap(right_image_undistorted, map_right_x, map_right_y, cv2.INTER_LINEAR)

    # Call the constructor for StereoBM
    stereo = cv2.StereoSGBM_create(numDisparities =16*5 , blockSize =21)
    # Calculate the disparity image
    disparity = stereo.compute(remapped_left, remapped_right)

    #disparity = stereo.compute(left_image_undistorted, right_image_undistorted)

    # -- Display as a CV_8UC1 image
    disp = None
    disp = cv2.normalize(src=disparity, dst=disp, beta=0, alpha =255, norm_type = cv2.NORM_MINMAX) 
    disp = np.uint8(disp)

    coords_3d=cv2.reprojectImageTo3D(disparity, Q)

    coords_3d=coords_3d.reshape(-1,3)
    filtered_coords=[]

    for i in range(coords_3d.shape[0]):
       if np.all(~np.isinf(coords_3d[i])) and coords_3d[i][2]>1 and coords_3d[i][2]<3:
           filtered_coords.append(coords_3d[i])

    pcd = o3d.geometry.PointCloud()
    pcd.points=o3d.utility.Vector3dVector(filtered_coords)
    o3d.visualization.draw_geometries([pcd])

    cv2.imshow("image left", left_image)
    cv2.imshow("Disparity Map", disp)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()