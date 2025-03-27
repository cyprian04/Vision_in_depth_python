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

    def menu(self):
        print("[OPTION 1] Press 1 to exctract rgb frames")
        print("[OPTION 2] Press 2 to exctract depth frames")
        print("[OPTION 3] Press 3 to exctract point_clouds")
        print("[OPTION 4] Press 4 to playback rgb video")
        print("[OPTION 5] Press 5 to playback depth video")
        print("[OPTION 6] Press 6 to exit")
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
                self.run = False
                os.system("cls")
            case _:
                print("Wrong option! try again...")

    def get_run(self):
        return self.run

    def get_rgb(self):
        pass

    def get_depth(self):
        pass

    def get_point_cloud(self):
        '''extract point_clouds from frames in compressed format: numpy array (w,h,6) -> [x,y,z,r,g,b]'''
        extracted_folder = "extracted"
        os.makedirs(extracted_folder, exist_ok=True)

        point_clouds = []
        frame_count = 0

        key = ''
        runtime = sl.RuntimeParameters()
        rgb = sl.Mat()
        xyz = sl.Mat()

        self.cam.set_svo_position(1000) # for tests only, change LATER !!!
        while key != ord('q'): 
            err = self.cam.grab(runtime)
            if err == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
                break

            self.cam.retrieve_image(rgb, sl.VIEW.LEFT)
            rgb_np = rgb.get_data()[:, :, :3].astype(np.float32)

            self.cam.retrieve_measure(xyz, sl.MEASURE.XYZRGBA)
            xyz_np = xyz.get_data()[:, :, :3].astype(np.float32)

            point_cloud = np.stack([xyz_np[:, :, 0], xyz_np[:, :, 1], xyz_np[:, :, 2], rgb_np[:, :, 0], rgb_np[:, :, 1], rgb_np[:, :, 2]], axis=-1).astype(np.float32)
            point_clouds.append(point_cloud)  


            print(f"Klatka nr:{frame_count} pobrana")
            frame_count += 1

            if frame_count % 100 == 0:
                part_file_path = os.path.join(extracted_folder, f"point_clouds_part_{frame_count // 100}.npz")
                point_clouds_array = np.array(point_clouds, dtype=np.float32)
                np.savez_compressed(part_file_path, data=point_clouds_array)
                print(f"Zapisano {len(point_clouds)} klatek do {part_file_path}")
                point_clouds = [] 

            if frame_count == 100:  
                break

        zip_path = os.path.join(extracted_folder, "all_point_clouds.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(extracted_folder):
                if file.endswith(".npz"):
                    zipf.write(os.path.join(extracted_folder, file), file)
        print(f"Zapisano dane w formacie zip: {zip_path}")

        cv2.destroyAllWindows()
        self.cam.close()

    def play_rgb_video(self):
        key = ''
        runtime = sl.RuntimeParameters()
        image = sl.Mat()

        while key != ord('q'): 
            if self.cam.grab(runtime) == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
                break

            self.cam.retrieve_image(image, sl.VIEW.LEFT)
            img_np = image.get_data()
        cv2.imshow("image", img_np)
        key = cv2.waitKey(1)

        cv2.destroyAllWindows()
        self.cam.close()

    def play_depth_video(self):
        key = ''
        runtime = sl.RuntimeParameters()
        depth = sl.Mat()

        while key != ord('q'): 
            if self.cam.grab(runtime) == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
                break

            self.cam.retrieve_image(depth, sl.VIEW.DEPTH)
            depth_np = depth.get_data()
            
        cv2.imshow("depth", depth_np)
        key = cv2.waitKey(1)

        cv2.destroyAllWindows()
        self.cam.close()
