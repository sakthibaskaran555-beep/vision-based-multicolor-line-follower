import cv2
import numpy as np
import serial
import time

# Initialize UART communication with ESP32
esp32 = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to initialize

# Initialize the camera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Try DSHOW for Windows, V4L2 for Linux
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 60)

# Constants for frame width and thresholding
FRAME_WIDTH = 320
FRAME_CENTER = FRAME_WIDTH // 2
LEFT_THRESHOLD = FRAME_CENTER - 50
RIGHT_THRESHOLD = FRAME_CENTER + 50
SHARP_TURN_THRESHOLD = 250  # Y-coordinate threshold for sharp turn detection

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # === Define the GREEN color range ===
    lower_green = np.array([40, 50, 50])  # Adjust values based on lighting conditions
    upper_green = np.array([90, 255, 255])

    # Create mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Apply morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])  # Centroid X
            cy = int(M['m01'] / M['m00'])  # Centroid Y

            # Draw the centroid
            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)

            # **Sharp turn detection**
            if cy > SHARP_TURN_THRESHOLD:
                if cx < LEFT_THRESHOLD:
                    print("Sharp Left Turn")
                    esp32.write(b'Q')  # Custom sharp left command
                elif cx > RIGHT_THRESHOLD:
                    print("Sharp Right Turn")
                    esp32.write(b'E')  # Custom sharp right command
                time.sleep(0.3)  # Slightly longer delay for sharp turns

            # **Regular movement**
            elif cx < LEFT_THRESHOLD:
                print("Turn Left")
                esp32.write(b'L')
                #time.sleep(0.3)
            elif cx > RIGHT_THRESHOLD:
                print("Turn Right")
                esp32.write(b'R')
                #time.sleep(0.3)
            else:
                print("On Track!")
                esp32.write(b'F')
                #time.sleep(0.3)

        else:
            print("Lost line! Stopping...")
            esp32.write(b'S')  # Stop if no centroid is found

    else:
        print("No line detected! Stopping...")
        esp32.write(b'S')

    # Display the frames
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
esp32.close()
