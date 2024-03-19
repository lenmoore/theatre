from printers import print_current_prompt
import cv2
import os
import base64

# Function to encode the image
def encode_image(image_path='pictures/photo.jpg'):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def read_from_arduino():
    global style, setting, drama, comedy
    while ser.inWaiting() > 0:  # Check if data is available
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("STYLE"):
            index = int(line.replace("STYLE", ""))
            styles = ["Romeo and Juliet", "Sopranos", "Star Trek"]
            style = styles[index]
            print_current_prompt(setting, style, drama, comedy)
        elif line.startswith("SCENE"):
            index = int(line.replace("SCENE", ""))
            settings = ["Mars", "Hairdresser", "Classroom"]
            setting = settings[index]
            print_current_prompt(setting, style, drama, comedy)
        elif line.startswith("DRAMA"):
            drama = int(line.replace("DRAMA", ""))
            print_current_prompt(setting, style, drama, comedy)
        elif line.startswith("COMEDY"):
            comedy = int(line.replace("COMEDY", ""))
            print_current_prompt(setting, style, drama, comedy)
        elif line == "START":
            return True  # Start button pressed
    return False  # Start button not pressed


def capture_image(filename='photo.jpg'):
    cap = cv2.VideoCapture(0) # check this
#     cap = cv2.VideoCapture("/dev/video2") # check this
    ret, frame = cap.read()
    if ret:
        if not os.path.exists('pictures'):
            os.makedirs('pictures')
        cv2.imwrite(os.path.join('pictures', filename), frame)

    cap.release()
    return ret
