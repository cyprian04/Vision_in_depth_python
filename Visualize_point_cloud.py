import numpy as np
import open3d as o3d
import os

def visualize_point_clouds(npz_file):
    if not os.path.exists(npz_file):
        print(f"Plik {npz_file} nie istnieje!")
        return
    
    data = np.load(npz_file)["data"]
    print(f"Załadowano dane: {data.shape}")
    
    
    frame_index = 11 
    point_cloud = data[frame_index]
    
    # Pobranie współrzędnych 3D i kolorów
    xyz = point_cloud[:, :, :3].reshape(-1, 3)  # Pozycje 3D
    rgb = point_cloud[:, :, 3:].reshape(-1, 3) / 255.0  # Normalizacja kolorów
    rgb = rgb[:, [2, 1, 0]]  # Zamiana BGR -> RGB

    
    #Sprawdzam NaN i ustawiam na 0
    nan_mask = np.isnan(xyz[:, 2])
    if np.any(nan_mask):
        print(f"⚠️ Znaleziono {nan_mask.sum()} NaN w głębi! Usuwam je...")
        xyz[nan_mask, 2] = 0
    # Zakres głębi po usunięciu NaN
    print(f"Zakres głębi (z): min={xyz[:,2].min()}, max={xyz[:,2].max()}")
        

    valid_mask = xyz[:, 2] != 0
    xyz = xyz[valid_mask]
    rgb = rgb[valid_mask]
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.colors = o3d.utility.Vector3dVector(rgb)
    pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=10, std_ratio=2.0) # Filtracja outlierów (usuwa "odstające" punkty), bez tego wygląda gorzej
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    npz_file = "extracted/point_clouds_neural_plus.npz"
    visualize_point_clouds(npz_file)
