import numpy as np
import open3d as o3d

def visualize(npz_file):
    '''
    Responsible for visualizing the pcd in open3d enviroment
    '''
    
    data = np.load(npz_file)["data"]
    print(f"[INFO] Loaded data: {data.shape}")
    
    frame_index = 11 
    point_cloud = data[frame_index]
    
    # Pobranie współrzędnych 3D i kolorów
    xyz = point_cloud[:, :, :3].reshape(-1, 3)  # Pozycje 3D
    rgb = point_cloud[:, :, 3:].reshape(-1, 3) / 255.0  # Normalizacja kolorów
    rgb = rgb[:, [2, 1, 0]]  # Zamiana BGR -> RGB

    
    nan_mask = np.isnan(xyz[:, 2])
    if np.any(nan_mask):
        print(f"Znaleziono {nan_mask.sum()} NaN w głębi! Usuwam je...")
        xyz[nan_mask, 2] = 0

    print(f"Zakres głębi (z): min={xyz[:,2].min()}, max={xyz[:,2].max()}")
        

    valid_mask = xyz[:, 2] != 0
    xyz = xyz[valid_mask]
    rgb = rgb[valid_mask]
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.colors = o3d.utility.Vector3dVector(rgb)
    pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=10, std_ratio=2.0)
    o3d.visualization.draw_geometries([pcd])
