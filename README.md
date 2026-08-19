# Vision-Based Multi-Color Line Follower Robot

A vision-based autonomous line-following robot that detects and follows **red, green, and black lines** using **Python, OpenCV, a USB camera, and ESP32**.

The laptop performs real-time image processing using OpenCV. Based on the detected line position, movement commands are sent to the ESP32 through serial communication. The ESP32 controls two N20 geared motors using an L298N motor driver.

## Project Overview

This project demonstrates the use of computer vision and embedded systems to build an autonomous line-following robot.

A USB camera captures the path in front of the robot. The camera feed is processed on a laptop using Python and OpenCV. The system detects the selected line color, finds its position, and determines the required direction.

The movement command is then transmitted to the ESP32 through serial communication.

The ESP32 receives the command and controls the N20 geared motors through the L298N motor driver.

## Features

* Red line detection
* Green line detection
* Black line detection
* Real-time camera-based image processing
* OpenCV-based computer vision
* Centroid-based line tracking
* Left and right turning
* Sharp turn detection
* Serial communication between laptop and ESP32
* N20 geared motor control
* L298N motor driver

## Hardware Used

| Component            | Purpose                |
| -------------------- | ---------------------- |
| ESP32                | Motor control          |
| USB Camera / Webcam  | Captures the path      |
| Laptop               | Image processing       |
| L298N Motor Driver   | Controls the motors    |
| N20 Geared Motors    | Robot movement         |
| Robot Chassis        | Mechanical structure   |
| Adapter Power Supply | Provides power         |
| Connecting Wires     | Electrical connections |

**Note:** The robot is powered using an external adapter power supply rather than a battery.

## Software Used

* Python
* OpenCV
* NumPy
* PySerial
* Arduino IDE
* ESP32

## System Architecture

```text
                 USB Camera
                     |
                     v
              +-------------+
              |   Laptop    |
              | Python +    |
              |   OpenCV    |
              +------+------+
                     |
              Line Detection
                     |
              Centroid Position
                     |
              Direction Decision
                     |
             Serial Communication
                     |
                     v
                +---------+
                |  ESP32  |
                +----+----+
                     |
                     v
                +---------+
                |  L298N  |
                +----+----+
                     |
              +------+------+
              |             |
              v             v
          N20 Motor      N20 Motor
              |             |
              +------+------+
                     |
                     v
               Robot Motion
```

## Working Principle

### 1. Camera Capture

The USB camera continuously captures the path in front of the robot.

The laptop processes the camera feed using OpenCV.

The camera is configured to use a resolution of approximately 320 × 240 pixels.

### 2. Color Detection

For red and green line detection, the camera frame is converted from BGR to HSV color space.

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

HSV thresholding is then used to create a mask for the selected color.

### 3. Black Line Detection

For black-line detection, the image is converted to grayscale and thresholded.

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

_, mask = cv2.threshold(
    gray,
    40,
    255,
    cv2.THRESH_BINARY_INV
)
```

### 4. Noise Removal

Morphological operations are used to reduce noise in the detected mask.

```python
kernel = np.ones((5, 5), np.uint8)

mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
```

### 5. Centroid Detection

The largest detected contour is selected and its centroid is calculated using image moments.

```python
M = cv2.moments(c)

cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])
```

The horizontal centroid position is used to determine whether the robot should move left, right, or forward.

## Movement Commands

| Command | Action      |
| ------- | ----------- |
| `F`     | Forward     |
| `L`     | Turn Left   |
| `R`     | Turn Right  |
| `Q`     | Sharp Left  |
| `E`     | Sharp Right |
| `S`     | Stop        |

Example:

```python
esp32.write(b'F')
```

This sends the forward command to the ESP32.

## Project Structure

```text
vision-based-multicolor-line-follower/
|
├── README.md
├── .gitignore
├── LICENSE
├── requirements.txt
|
├── python/
|   ├── red_line_follower.py
|   ├── green_line_follower.py
|   └── black_line_follower.py
|
├── esp32/
|   └── motor_controller.ino
|
├── images/
|   └── robot.jpg
|
└── videos/
    └── robot-demo.mp4
```

## Installation

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

Required libraries:

```text
opencv-python
numpy
pyserial
```

## How to Run

### 1. Upload ESP32 Code

Open the following file in Arduino IDE:

```text
esp32/motor_controller.ino
```

Select the appropriate ESP32 board and upload the code.

### 2. Connect the ESP32

Connect the ESP32 to the laptop through USB.

The Python program currently uses:

```python
esp32 = serial.Serial('COM4', 9600, timeout=1)
```

Change `COM4` to the COM port assigned to your ESP32.

### 3. Connect the Camera

Connect the USB camera to the laptop.

The current program uses:

```python
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
```

Change the camera index if required.

### 4. Run the Python Program

For red-line detection:

```bash
python python/red_line_follower.py
```

For green-line detection:

```bash
python python/green_line_follower.py
```

For black-line detection:

```bash
python python/black_line_follower.py
```

Press **Q** to exit the program.

## Robot Image

Add the robot image to the `images` folder and name it `robot.jpg`.

Then it will appear here:

![Vision-Based Multi-Color Line Follower Robot](images/robot.jpg)

## Demonstration Video

A demonstration video of the robot following the line is included in the project.

Video file:

```text
videos/robot-demo.mp4
```

## Results

The prototype successfully demonstrated vision-based line following using a laptop, camera, OpenCV, ESP32, and motor-control hardware.

The robot was able to:

* Detect red, green, and black lines
* Follow straight paths
* Perform left and right turns
* Detect sharp turns
* Send movement commands from the laptop to the ESP32
* Control N20 geared motors through the L298N motor driver

## Future Improvements

* PID-based steering control
* Automatic color calibration
* Adaptive thresholding
* Improved performance under changing lighting conditions
* Wireless communication between laptop and ESP32
* On-board image processing
* Obstacle detection
* Automatic speed adjustment
* Intersection detection

## Technologies

`Python` `OpenCV` `NumPy` `PySerial` `ESP32` `Arduino` `L298N` `N20 Geared Motor` `Computer Vision` `Robotics`

## Project Type

**Mini Project – Robotics, Computer Vision and Embedded Systems**
