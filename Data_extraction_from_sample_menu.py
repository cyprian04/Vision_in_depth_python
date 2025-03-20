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
    print("Press 3 to extract data from frames in compressed format [x,y,z,r,g,b] via numpy\n")
    return int(input("Option: "))


def main(option:int):
    filepath = opt.input_svo_file # Path to the .svo file to be playbacked
    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)  #Set init parameter to run from the .svo 
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE 
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS: #Ensure the camera opened succesfully 
        print("Camera Open", status, "Exit program.")
        exit(1)

    print(f"[Info] SVO contains {cam.get_svo_number_of_frames()} frames")
    print(f"[Info] SVO contains {cam.get_init_parameters().camera_fps} frame rate")
    print(" Press 'q' to exit...")
    key = ''

    # Set a maximum resolution, for visualisation confort 
    runtime = sl.RuntimeParameters()
    resolution = cam.get_camera_information().camera_configuration.resolution
    image = sl.Mat(min(720,resolution.width) * 2,min(404,resolution.height), sl.MAT_TYPE.U8_C3, sl.MEM.CPU)
    #depth = sl.Mat()
    runtime = sl.RuntimeParameters()

    while key != ord('q'): # for 'q' key
        err = cam.grab(runtime)

        # Pobranie klatki RGB
        cam.retrieve_image(image, sl.VIEW.LEFT)
        img_np = image.get_data()[:, :, :3]  # Ignorujemy kanał Alpha

        # Pobranie mapy głębi
        #cam.retrieve_measure(depth, sl.MEASURE.DEPTH)
        #depth_np = depth.get_data()

        # Konwersja do formatu [x, y, z, r, g, b]
        #h, w, _ = img_np.shape
        #x, y = np.meshgrid(np.arange(w), np.arange(h))  # Pozycje pikseli w obrazie
        #z = depth_np  # Głębia

        # Łączenie w tablicę numpy
        #point_cloud = np.stack([x, y, z, img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]], axis=-1)

        # Zapisywanie danych dla tej klatki
        #np.savez_compressed(f"frame_{cam.get_timestamp(sl.TIME_REFERENCE.CURRENT).get_milliseconds()}.npz", data=point_cloud)

        # Podgląd obrazu
        cv2.imshow("image", img_np)
        key = cv2.waitKey(1)

        if err == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
            break

    cv2.destroyAllWindows()
    cam.close()


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
