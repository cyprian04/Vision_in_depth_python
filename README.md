# Vision in depth Python

This project allows you to work with `.svo` files from a ZED camera, extract RGB images, depth maps and point clouds, as well as play video and visualize point clouds in 3D.
---


## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [File structure](#file-structure)
4. [Running the program](#running-the-program)
5. [Link to detailed documentation](#link-to-detailed-documentation)

---

## Requirements

* Operating system: Windows (tested only on Windows and some lines are hard coded for Windows for now)
* Python 3.11
* Installed ZED SDK and its dependencies from the [official website](https://www.stereolabs.com/en-pl/developers/release).
* Installed dependencies from [`requirements.txt`](requirements.txt).

---

## Installation

1. clone the repository or copy the project folder to your local disk.
2. open a terminal (PowerShell) and navigate to the root directory of the project:

   ```bash
   cd /path/to/project
   ```
3. (Optional) Create and activate the virtual environment:

   ```bash
   python -m venv venv
   venv/cripts/activate # Windows PowerShell.
   ```
4. Install the packages from `requirements.txt`:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. make sure the ZED SDK is properly installed and configured.

6. If you have problems installing dependencies for this program or need a newer version of them, then
   more information can be found at [Python API for the ZED SDK](https://github.com/stereolabs/zed-python-api) official repository on github.

---

## File structure

```
/  
├─── main.py # The main script that calls the interface
├─── ZedPlayer.py # Class that manages operations on the .svo file
├─── Visualize_point_cloud.py # Function to visualize point clouds in 3D
├─── requirements.txt # List of required Python libraries
├─── README.md # This file
└─── documentation.md # Detailed documentation of modules and functions
```

* **main.py**: The main menu of the program, allows you to choose and load the `.svo` file or visualize the finished point cloud.
* **ZedPlayer.py**: `ZedPlayer` class for RGB, depth, point cloud extraction, video playback and RGB → MP4 conversion.
* **Visualize_point_cloud.py**: Function `visualize(npz_file)` to load a saved point cloud (`.npz` file) and display it in the Open3D environment.
* **requirements.txt**: List of versions of libraries required for the project to work.
* **documentation.md**: Extensive documentation of all modules and functions (link below).

---

## Running the program

1. Make sure you have all the dependencies installed and (optionally) the virtual environment configured.

2. In the terminal (PowerShell), navigate to the folder with the code and run:

   ```bash
   python main.py
   ```
3. the main menu will be displayed:

   ```
   [WELCOME TO VISION IN DEPTH PROJECT] choose one of the options listed below....

   [OPTION 1] Press 1 if you want to operate on video sample
   [OPTION 2] Press 2 to visualize in 3D already extracted point clouds from a file
   [OPTION 3] Press 3 to exit the program
   Option:
   ```

4. Enter the appropriate digit (1 / 2 / 3) and confirm with Enter.

### Options:

* **1**: Select `.svo` file and perform operations (RGB extraction, depth, clouds, video playback, conversion to MP4).
* **2**: Select `.npz` file (previously created point cloud) and display it in Open3D.
* **3**: Close the program.

---

## Link to detailed documentation

For a full description of classes, methods and file formats, see **[documentation.md](documentation.md)**.
