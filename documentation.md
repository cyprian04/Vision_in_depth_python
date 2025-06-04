# 📄 Vision in Depth project documentation.

This file contains detailed information about the features, classes and options available in the **Vision in Depth** project.

---

## Table of Contents

* [1. Main program options](#1-main-program-options)
* [2. ZedPlayer class ](#2-zedplayer-class)
* [3. Point cloud visualization](#3-visualize-point-cloud-file)
* [4. Requirements (`requirements.txt`)](#4-requirements-requirementstxt)

---

## 1. Main program options

After starting the main program (`main.py`), the user sees the menu:

```
[OPTION 1] Press 1 if you want to operate on video sample
[OPTION 2] Press 2 to visualize in 3D already extraced point clouds from a file
[OPTION 3] Press 3 to exit the program
```


### [1] Operation on `.svo` file

Opening the `ZedPlayer` menu, allows you to:

* RGB or depth frame extraction.
* RGB or depth video playback.
* Extraction of point clouds from the selected frame range.
* Conversion of all RGB frames to `.mp4` file.

### [2] Point cloud visualization (`.npz`)

You can select `.npz` file containing an array of `data`, where each frame is of the form `H x W x 6`:

* First 3 channels: XYZ coordinates.
* The last 3 channels: RGB

One frame is selected (example index 11, can change it manually), which is cleaned from NaN/0 and displayed in Open3D.

---

## 2. ZedPlayer class

The class manages all operations on the `.svo` file.

### Constructor

```python
ZedPlayer(filepath: str)
```

* Creates a `.svo` file object and initializes the ZED camera with depth mode `NEURAL_PLUS`.
* If it's too slow then change manually the mode to: `PERFORMANCE`

### Helper methods

* `menu()` - calls the options menu (see below).
* `close_cam()` - closes the camera.
* `get_run()` - checks if it is still running.

### Options in the ZedPlayer menu

```
[OPTION 1] Press 1 to exctract rgb frames
[OPTION 2] Press 2 to exctract depth frames
[OPTION 3] Press 3 to exctract point_clouds
[OPTION 4] Press 4 to playback rgb video
[OPTION 5] Press 5 to playback depth video
[OPTION 6] Press 6 to convert rgb frames to video
[OPTION 7] Press 7 to exit
```

#### \[1] `get_rgb()`

Selection of one frame → saving to `image.png`.

#### \[2] `get_depth()`

Selection of one frame → saving to `depth.jpg` (without NaN and inf)

#### \[3] `get_point_cloud()`

Selecting a range of frames → extracting point clouds and saving:

* Partial `.npz` in `extracted` folder.
* Compression of all to one `all_point_clouds.zip`.

#### \[4] `play_rgb_video()`

Plays RGB from the beginning (`q` button ends).

#### \[5] `play_depth_video()`

Plays depth from the beginning (`q` button ends)

#### \[6] `convert_rgb_frames_to_video()`

Saves all RGB as `output.mp4`.

#### \[7] `exit`

Ends the operation of ZedPlayer

---

## 3. Visualize point cloud file

### Function:

```python
def visualize(npz_file: str)
```

* Loads `.npz` data with a 4D array `data: (num_frames, H, W, 6)`.
* Uses frame `data[11]` as an example.
* Removes NaN and depth `z=0`.
* Displays the cloud in Open3D with RGB colors.

---

## 4. Requirements (`requirements.txt`)

```txt
Cython==3.0.12
numpy==1.26.4
opencv-python==4.11.0.86
pillow==11.1.0
PyOpenGL==3.1.6
open3D==0.19.0
pyzed==4.2
```

* Needed environment: Python 3.11, system with compatible NVIDIA card and ZED 4.2 SDK installed
* Note: that program as it is was only tested on pyzed 4.2 and its corresponing version of CUDA (which is a dependency for ZED SDK). All informations about CUDA versions and more are mentioned on [official website](https://www.stereolabs.com/en-pl/developers/)

---

## ✨ Author

A project created by Cyprian Gibas in an exploration of depth and point cloud technology using a ZED camera and OpenCV/Open3D.
