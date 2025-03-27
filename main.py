import os
import ZedPlayer
import Visualize_point_cloud as visualize_pcd

#print("[OPTION 3] Press 3 to extract data from frames in compressed format np array (w,h,6) -> [x,y,z,r,g,b] via numpy")

def start_menu():
    print("[OPTION 1] Press 1 if you want to operate on video sample")
    print("[OPTION 2] Press 2 to visualize in 3D already extraced point clouds from a file")
    print("[OPTION 3] Press 3 to exit the program")
    return input("Option: ")

def main(run_state:dict):

    option = start_menu()
    os.system('cls')

    match option:
        case "1":
            while True:
                filepath = input("Enter filepath: ")
                if not os.path.exists(filepath):
                    os.system('cls')
                    print(f"File {filepath} doesn't exist!")
                    continue
                else: break

            player = ZedPlayer(filepath)
            while player.get_run():
                player.menu()  

        case "2":
            while True:
                filepath = input("Enter filepath: ")
                if not os.path.exists(filepath):
                    os.system('cls')
                    print(f"File {filepath} doesn't exist!")
                    continue
                else: break
            visualize_pcd.visualize(filepath) 

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