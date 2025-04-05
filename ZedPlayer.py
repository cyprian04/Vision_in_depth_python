import os
import sys
import cv2
import zipfile
import numpy as np
import pyzed.sl as sl

class ZedPlayer:
    def __init__(self, filepath):
        self.run = True
        self.filepath = filepath

        input_type = sl.InputType()
        input_type.set_from_svo_file(self.filepath)
        init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
        init.depth_mode = sl.DEPTH_MODE.NEURAL_PLUS # this mode will put a strain on the GPU. Choose PERFORMANCE for less strain

        self.cam = sl.Camera()
        self.status = self.cam.open(init)
        if self.status != sl.ERROR_CODE.SUCCESS: 
            print("Camera Open", self.status, "Exit program.")
            exit(1)

        print(f"[INFO] SVO contains {self.cam.get_svo_number_of_frames()} frames")
        print(f"[INFO] SVO runs at {self.cam.get_init_parameters().camera_fps} frames per second")
        print("[SUCCESS] Successfully created ZedPlayer instance")
        input("Press ENTER to continue...")
        os.system("cls")

    def menu(self):
        print("[OPTION 1] Press 1 to exctract rgb frames")
        print("[OPTION 2] Press 2 to exctract depth frames")
        print("[OPTION 3] Press 3 to exctract point_clouds")
        print("[OPTION 4] Press 4 to playback rgb video")
        print("[OPTION 5] Press 5 to playback depth video")
        print("[OPTION 6] Press 6 to convert rgb frames to video")
        print("[OPTION 7] Press 7 to exit")
        option =  input("Option: ")

        match option:
            case "1":
                self.get_rgb()
            case "2":
                self.get_depth()
            case "3":
                self.get_point_cloud()
            case "4":
                self.play_rgb_video()
            case "5":
                self.play_depth_video()
            case "6":
                self.convert_rgb_frames_to_video()
            case "7":
                self.run = False
                os.system("cls")
            case _:
                input("Wrong option! press Enter to try again...")
        os.system("cls")
    
    def close_cam(self):
        self.cam.close()
        self.cam = None

    def get_run(self):
        return self.run

    def get_rgb(self):
        image = sl.Mat()
        while True:
            os.system("cls")
            try:            
                frame = int(input("Enter frame index to extract: "))
                if frame >= 0 and frame < self.cam.get_svo_number_of_frames():
                       break
                else:
                    input("[INFO] Bad range, press ENTER to try again...")
            except ValueError:
                input("[INFO] Bad range, press ENTER to try again...")
                continue

        self.cam.set_svo_position(frame)        
        self.cam.grab(sl.RuntimeParameters())
        self.cam.retrieve_image(image, sl.VIEW.LEFT)
        img_np = image.get_data()[:, :, :3].astype(np.float32)
        cv2.imwrite("image.png", img_np)
        cv2.waitKey(1)
        cv2.destroyAllWindows()

    def get_depth(self):
        depth = sl.Mat()
        while True:
            os.system("cls")
            try:            
                frame = int(input("Enter frame index to extract: "))
                if frame >= 0 and frame < self.cam.get_svo_number_of_frames():
                       break
                else:
                    input("[INFO] Bad range, press ENTER to try again...")
            except ValueError:
                input("[INFO] Bad range, press ENTER to try again...")
                continue

        self.cam.set_svo_position(frame)        
        self.cam.grab(sl.RuntimeParameters())
        self.cam.retrieve_image(depth, sl.VIEW.DEPTH)
        depth_np = depth.get_data()

        depth_np[np.isnan(depth_np)] = 0
        depth_np[np.isinf(depth_np)] = 0
    
        cv2.imwrite("depth.jpg", depth_np)
        cv2.waitKey(1)
        cv2.destroyAllWindows()

    def get_point_cloud(self):
        '''
        Extract point clouds from selected frames and compress them into a folder.
        '''
        extracted_folder = "extracted"
        os.makedirs(extracted_folder, exist_ok=True)

        while True:
            os.system("cls")
            try:
                start_frame = int(input("Enter the index of start frame: "))
                end_frame = int(input("Enter the index of the end frame: "))
                if start_frame >= 0 and end_frame > start_frame and end_frame < self.cam.get_svo_number_of_frames():
                    break
                else:
                    input("[INFO] Bad range, press ENTER to try again...")
            except ValueError:
                input("[INFO] Bad range, press ENTER to try again...")
                continue

        point_clouds = []
        frame_count = 0
        
        runtime = sl.RuntimeParameters()
        rgb = sl.Mat()
        xyz = sl.Mat()

        self.cam.set_svo_position(start_frame) 

        while True:
            err = self.cam.grab(runtime)
            if err == sl.ERROR_CODE.END_OF_SVOFILE_REACHED or (start_frame + frame_count) >= end_frame:
                break 

            self.cam.retrieve_image(rgb, sl.VIEW.LEFT)
            rgb_np = rgb.get_data()[:, :, :3].astype(np.float32)

            self.cam.retrieve_measure(xyz, sl.MEASURE.XYZRGBA)
            xyz_np = xyz.get_data()[:, :, :3].astype(np.float32)

            point_cloud = np.dstack((xyz_np, rgb_np)).astype(np.float32)
            point_clouds.append(point_cloud)

            print(f"Frame nr: {start_frame + frame_count} retrieved")
            frame_count += 1

            if frame_count % 100 == 0 or (start_frame + frame_count) >= end_frame:
                part_file_path = os.path.join(extracted_folder, f"point_clouds_part_{(start_frame + frame_count) // 100}.npz")
                point_clouds_array = np.array(point_clouds, dtype=np.float32)
                np.savez_compressed(part_file_path, data=point_clouds_array)
                print(f"[SUCCESS] Saved {len(point_clouds)} frames to: {part_file_path}")
                point_clouds = []  
        
        print("[INFO] Ended the process of compresion of each frame, please wait, now the all stages (.npz) will be compressed all together to zip file")

        zip_path = os.path.join(extracted_folder, "all_point_clouds.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(extracted_folder):
                if file.endswith(".npz"):
                    zipf.write(os.path.join(extracted_folder, file), file)
        print(f"[SUCCESS] Saved data in zip format: {zip_path}")
        input(f"[INFO] Press ENTER to continue...")
        cv2.destroyAllWindows()

    def play_rgb_video(self):
        key = ''
        runtime = sl.RuntimeParameters()
        image = sl.Mat()
        self.cam.set_svo_position(0)

        while key != ord('q'): 
            if self.cam.grab(runtime) == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
                break
            self.cam.retrieve_image(image, sl.VIEW.LEFT)
            img_np = image.get_data()

            cv2.imshow("image", img_np)
            key = cv2.waitKey(1)

        cv2.destroyAllWindows()

    def play_depth_video(self):
        key = ''
        runtime = sl.RuntimeParameters()
        depth = sl.Mat()
        self.cam.set_svo_position(0)

        while key != ord('q'): 
            if self.cam.grab(runtime) == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
                break
            self.cam.retrieve_image(depth, sl.VIEW.DEPTH)
            depth_np = depth.get_data()
            
            cv2.imshow("depth", depth_np)
            key = cv2.waitKey(1)

        cv2.destroyAllWindows()

    def convert_rgb_frames_to_video(self, output_filename="output.mp4"):
        """
        Extracts all RGB frames from the SVO file and writes them to a video file.
        """
        num_frames = self.cam.get_svo_number_of_frames()
        fps = self.cam.get_init_parameters().camera_fps

        image = sl.Mat()
        runtime = sl.RuntimeParameters()
        self.cam.set_svo_position(0)
        
        self.cam.retrieve_image(image, sl.VIEW.LEFT)
        frame_np = image.get_data()[:, :, :3]
        height, width, _ = frame_np.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

        for frame_index in range(num_frames):
            if self.cam.grab(runtime) == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
                break   
            self.cam.retrieve_image(image, sl.VIEW.LEFT)
            image_np = image.get_data()[:, :, :3]
            video_writer.write(image_np)
            print(f"[INFO] Frame {frame_index+1}/{num_frames} written")
        
        video_writer.release()
        input(f"[SUCCESS] Video saved as {output_filename}. Press ENTER to continue...")