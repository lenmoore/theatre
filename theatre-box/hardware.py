from printers import print_current_prompt
import cv2
import os
import serial
import time
from time import sleep
from printers import pretty_print, print_current_prompt, print_section
import os
import base64
import cv2

from dotenv import load_dotenv
load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT")


# Initialize serial port - replace 'COM3' with your Arduino's port
# UNCOMMENT TO ENABLE ARDUINO INTERACTION
ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)

# Function to encode the image
def encode_image(image_path='pictures/photo.jpg'):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def capture_image(filename='photo.jpg'):
#     cap = cv2.VideoCapture(0) # check this
    cap = cv2.VideoCapture("/dev/video2") # check this
    sleep(0.1) # camera wakes up

    ret, frame = cap.read()
    sleep(0.1) # camera wakes up

    if ret:
        if not os.path.exists('pictures'):
            os.makedirs('pictures')
        cv2.imwrite(os.path.join('pictures', filename), frame)

    cap.release()
    image_path = "pictures/photo.jpg"
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def adjust_camera_settings(camera_index):
    cap = cv2.VideoCapture(camera_index)

    # Set properties for brightness and contrast (modify values as needed)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.25)  # 0.0 to 1.0
    cap.set(cv2.CAP_PROP_CONTRAST, 14)    # 0.0 to 1.0
#     cap.set(cv2.CAP_PROP_FOCUS , 100)    # 0.0 to 1.0

    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Set frame rate
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Release the camera
    cap.release()

if __name__ == "__main__":

    # Call the function with the camera index (e.g., 0 for the first camera)
    adjust_camera_settings("/dev/video2")

    capture_image()
