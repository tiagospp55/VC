# Aula_07_exe_05.py
#
# ICP alignment
#
# Paulo Dias

import numpy as np
import open3d as o3d
import copy

def draw_registration_result_original_color(source, target, transformation):
    source_temp = copy.deepcopy(source)
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target])

source = o3d.io.read_point_cloud('./depth_Images/filt_office1.pcd')
target = o3d.io.read_point_cloud('./depth_Images/filt_office2.pcd')

# Create axes mesh
Axes = o3d.geometry.TriangleMesh.create_coordinate_frame(1)

# draw initial alignment
current_transformation = np.identity(4)
draw_registration_result_original_color(source, target, current_transformation)


# draw final alignment
current_transformation = np.identity(4)
voxel_size = 0.05
threshold = 8.0 * voxel_size

reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, 0.5)
        
print(reg_p2p.transformation)

#print(reg_p2p)
draw_registration_result_original_color(source, target, reg_p2p.transformation)
