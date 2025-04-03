import os
import tkinter as tk
from tkinter import filedialog
from ZedPlayer import ZedPlayer as Player
import Visualize_point_cloud as visualize_pcd


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

                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                filepath = filedialog.askopenfilename(title="Wybierz plik")

                if not os.path.exists(filepath):
                    os.system('cls')
                    print(f"[ERROR] File {filepath} doesn't exist! choose again!")
                    continue
                else: break

            player = Player(filepath)
            while player.get_run():
                player.menu()  
            player.close_cam()

        case "2":
            while True:
                
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                filepath = filedialog.askopenfilename(title="Wybierz plik")

                if not os.path.exists(filepath):
                    os.system('cls')
                    print(f"[ERROR] File {filepath} doesn't exist! choose again!")
                    continue
                else: break
            visualize_pcd.visualize(filepath) 

        case "3":
            run_state["run"] = False
        case _:
            input("Wrong option! press Enter to try again...")
    
if __name__ == "__main__":
    print("[WELCOME TO VISION IN DEPTH PROJECT] choose one of the options listed below...\n")
    run_state = {"run": True}
    while run_state["run"]:
        main(run_state)
    print("[CLOSING] Goodbye...")