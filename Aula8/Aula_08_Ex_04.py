 # viewcloud.py
 #
 # open3D examepl to view a point cloud
 #
 # Paulo Dias

import numpy as np
import open3d as o3d

office1 = o3d.io.read_point_cloud('depth_Images/filt_office1.pcd')
office2 = o3d.io.read_point_cloud('depth_Images/filt_office2.pcd')
# Create axes mesh
Axes = o3d.geometry.TriangleMesh.create_coordinate_frame(1)

# shome meshes in view
o3d.visualization.draw_geometries([office1, office2, Axes])



