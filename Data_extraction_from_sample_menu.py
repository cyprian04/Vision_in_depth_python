import os 
import sys
import cv2
import argparse
import numpy as np
import pyzed.sl as sl


def menu():
    print("[WELCOME] choose one of the below options\n")
    print("Press 1 to playback a sample video in RGB mode\n")
    print("Press 2 to playback a sample video in Depth mode\n")
    print("Press 3 to extract data from frames in compressed format np array (w,h,6) -> [x,y,z,r,g,b] via numpy\n")
    return int(input("Option: "))

def RGB_video(cam):
    key = ''
    runtime = sl.RuntimeParameters()
    resolution = cam.get_camera_information().camera_configuration.resolution
    image = sl.Mat(min(720,resolution.width) * 2,min(404,resolution.height), sl.MAT_TYPE.U8_C3, sl.MEM.CPU)

    while key != ord('q'): 
        if cam.grab(runtime) == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
            break

        cam.retrieve_image(image, sl.VIEW.LEFT)
        img_np = image.get_data()
       
        cv2.imshow("image", img_np)
        key = cv2.waitKey(1)

    cv2.destroyAllWindows()
    cam.close()

def Depth_video(cam):
    key = ''
    runtime = sl.RuntimeParameters()
    resolution = cam.get_camera_information().camera_configuration.resolution
    depth = sl.Mat(min(720,resolution.width) * 2,min(404,resolution.height), sl.MAT_TYPE.U8_C3, sl.MEM.CPU)

    while key != ord('q'): 
        if cam.grab(runtime) == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
            break

        cam.retrieve_image(depth, sl.VIEW.DEPTH)
        depth_np = depth.get_data()
        
        cv2.imshow("depth", depth_np)
        key = cv2.waitKey(1)

    cv2.destroyAllWindows()
    cam.close()
    
def Data_extraction_to_compressed_np(cam):
    extracted_folder = "extracted"
    os.makedirs(extracted_folder, exist_ok=True)  # Tworzymy folder jeśli nie istnieje

    point_clouds = []  # Lista na wszystkie klatki
    frame_count = 0;

    key = ''
    runtime = sl.RuntimeParameters()
    resolution = cam.get_camera_information().camera_configuration.resolution
    image = sl.Mat(min(720,resolution.width) * 2,min(404,resolution.height), sl.MAT_TYPE.U8_C3, sl.MEM.CPU)
    resolution = cam.get_camera_information().camera_configuration.resolution
    depth = sl.Mat(min(720,resolution.width) * 2,min(404,resolution.height), sl.MAT_TYPE.U8_C3, sl.MEM.CPU)

    while key != ord('q'):  # 'q' kończy pętlę
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
            break

        # Tworzymy chmurę punktów dla tej klatki
        if frame_count % 100 == 0: # later will get rid of it probably for now for small data
            # Pobranie klatki RGB
            cam.retrieve_image(image, sl.VIEW.LEFT)
            img_np = image.get_data()[:, :, :3].astype(np.float32)  # RGB (ignorujemy kanał Alpha)

            # Pobranie mapy głębi
            cam.retrieve_measure(depth, sl.MEASURE.DEPTH)
            depth_np = depth.get_data().astype(np.float32)

            # Konwersja do formatu [x, y, z, r, g, b]
            h, w, _ = img_np.shape
            x, y = np.meshgrid(np.arange(w), np.arange(h))  # Pozycje pikseli w obrazie
            z = depth_np  # Głębia
            point_cloud = np.stack([x, y, z, img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]], axis=-1).astype(np.float32)
            point_clouds.append(point_cloud)  # Dodajemy do listy

        
        print(f"Klatka nr:{frame_count} pobrana")
        frame_count+=1
        if frame_count == 1400: # for now, will change and fix later
            break

    # Konwersja listy na numpy array i zapisanie do skompresowanego pliku
    point_clouds = np.array(point_clouds, dtype=np.float32)  # Konwersja na numpy array
    save_path = os.path.join(extracted_folder, "point_clouds.npz")
    np.savez_compressed(save_path, data=point_clouds)

    print(f"Zapisano {len(point_clouds)} klatek do {save_path}")

    # Sprzątanie
    cv2.destroyAllWindows()
    cam.close()

def main(option:int):
    filepath = opt.input_svo_file # Path to the .svo file to be playbacked
    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)  #Set init parameter to run from the .svo 
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    init.depth_mode = sl.DEPTH_MODE.NEURAL_PLUS # can choose other types of modes
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS: #Ensure the camera opened succesfully 
        print("Camera Open", status, "Exit program.")
        exit(1)

    print(f"[Info] SVO contains {cam.get_svo_number_of_frames()} frames")
    print(f"[Info] SVO contains {cam.get_init_parameters().camera_fps} frame rate")
    print(" Press 'q' to exit...")

    match option:
        case 1:
            RGB_video(cam)
        case 2:
            Depth_video(cam)
        case 3:
            Data_extraction_to_compressed_np(cam)
        case _:
            print("Wrong option! try again...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_svo_file', type=str, help='Path to the SVO file', default="zed_video_sample.svo")
    opt = parser.parse_args()
    if not opt.input_svo_file.endswith(".svo") and not opt.input_svo_file.endswith(".svo2"): 
        print("--input_svo_file parameter should be a .svo file but is not : ",opt.input_svo_file,"Exit program.")
        exit()
    if not os.path.isfile(opt.input_svo_file):
        print("--input_svo_file parameter should be an existing file but is not : ",opt.input_svo_file,"Exit program.")
        exit()
    main(menu())
