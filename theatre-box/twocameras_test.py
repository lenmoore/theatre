from printers import prompt_print
import cv2
import os
import threading

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
            index = int(line.replace("SCENE", ""))
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


def capture_image(camera_index, output_filename):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # CAP_DSHOW is used to suppress a warning in some cases

    # Check if camera opened successfully
    if not cap.isOpened():
        print(f"Cannot open camera {camera_index}")
        return

    # Read an image
    ret, frame = cap.read()

    # Check if image is captured successfully
    if ret:
        # Save the image
        cv2.imwrite(output_filename, frame)
    else:
        print(f"Can't receive frame (stream end?). Exiting for camera {camera_index}")

    # When everything done, release the capture
    cap.release()



if __name__ == "__main__":
    # Define threads for each camera capture to minimize time difference
    thread1 = threading.Thread(target=capture_image, args=(0, 'image1.jpg'))  # Built-in webcam usually has index 0
    thread2 = threading.Thread(target=capture_image, args=(1, 'image2.jpg'))  # External USB webcam usually has index 1

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

