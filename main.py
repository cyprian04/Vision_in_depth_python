import os
import sys
import cv2
import zipfile
import argparse
import numpy as np
#import pyzed.sl as sl
#import ZedPlayer
import Visualize_point_cloud as visualize_pcd

# here handle file name in future, for now static
# visualize_pcd.visualize(npz_file = "extracted/point_clouds_part_1.npz")

def start_menu():
    print("[OPTION 1] Press 1 if you want to operate on existing video sample")
    print("[OPTION 2] Press 2 to visualize in 3D already extraced point clouds from a file")
    print("[OPTION 3] Press 3 to exit the program")
    #print("[OPTION 3] Press 3 to extract data from frames in compressed format np array (w,h,6) -> [x,y,z,r,g,b] via numpy")
    return input("Option: ")

def main(run_state:dict):
    '''
    filepath = "zed_video_sample.svo"
    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)  
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    init.depth_mode = sl.DEPTH_MODE.NEURAL_PLUS
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS: 
        print("Camera Open", status, "Exit program.")
        exit(1)

    print(f"[Info] SVO contains {cam.get_svo_number_of_frames()} frames")
    print(f"[Info] SVO contains {cam.get_init_parameters().camera_fps} frame rate")
    print(" Press 'q' to exit...")
    '''

    option = start_menu()
    os.system('cls')
    match option:
        case "1":
            print("first")            
        case "2":
            print("second")            
        case "3":
            run_state["run"] = False
        case _:
            print("Wrong option! try again...")

if __name__ == "__main__":
    print("[WELCOME TO VISION IN DEPTH PROJECT] choose one of the options listed below...\n")
    run_state = {"run": True}
    while run_state["run"]:
        main(run_state)
    print("[CLOSING] Goodbye...")
    
