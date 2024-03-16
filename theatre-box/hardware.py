from printers import prompt_print
import cv2
import os

def read_from_arduino():
    global style, setting, drama, comedy
    while ser.inWaiting() > 0:  # Check if data is available
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("STYLE"):
            index = int(line.replace("STYLE", ""))
            styles = ["Romeo and Juliet", "Sopranos", "Star Trek"]
            style = styles[index]
            prompt_print(setting, style, drama, comedy)
        elif line.startswith("SCENE"):
            index = int(line.replace("SC\ENE", ""))
            settings = ["Mars", "Hairdresser", "Classroom"]
            setting = settings[index]
            prompt_print(setting, style, drama, comedy)
        elif line.startswith("DRAMA"):
            drama = int(line.replace("DRAMA", ""))
            prompt_print(setting, style, drama, comedy)
        elif line.startswith("COMEDY"):
            comedy = int(line.replace("COMEDY", ""))
            prompt_print(setting, style, drama, comedy)
        elif line == "START":
            return True  # Start button pressed
    return False  # Start button not pressed


def capture_image(filename='photo.jpg'):
    cap = cv2.VideoCapture(0)  # Adjust the index if necessary
    ret, frame = cap.read()
    if ret:
        if not os.path.exists('pictures'):
            os.makedirs('pictures')
        cv2.imwrite(os.path.join('pictures', filename), frame)
    cap.release()
    return ret
