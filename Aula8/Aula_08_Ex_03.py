 # viewcloud.py
 #
 # open3D examepl to view a point cloud
 #
 # Paulo Dias

import numpy as np
import open3d as o3d
import cv2

with np.load('3DCoordinates.npz') as params:
    depth = params["depth"]
    Q = params["Q"]
    disparity = params["disparity"]
# Create array of random points between [-1,1]
pcl = o3d.geometry.PointCloud()
pcl.points = o3d.utility.Vector3dVector(np.random.rand(2500,3) * 2 - 1)
#pcl.paint_uniform_color([0.0, 0.0, 0.0])

# Create axes mesh
Axes = o3d.geometry.TriangleMesh.create_coordinate_frame(1)

# shome meshes in view
o3d.visualization.draw_geometries([pcl , Axes])

p = depth.reshape(-1, 3)
fp = []
for i in range(p.shape[0]):
    if np.all(~np.isinf(p[i])) and np.all(~np.isnan(p[i])):
        fp.append(p[i])
pcl = o3d.geometry.PointCloud()
pcl.points = o3d.utility.Vector3dVector(fp)
o3d.visualization.draw_geometries([pcl])

cv2.imshow("Disparity Map", disparity)
cv2.waitKey(0)
cv2.destroyAllWindows()


