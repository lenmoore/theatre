import serial
import cv2
import os
from time import sleep

style = "____"
setting = "____"
# Initialize serial port - replace 'COM3' with your Arduino's port
ser = serial.Serial('/dev/tty.usbmodem213401', 9600, timeout=1)

def pretty_print(message):
    print(f"\n=== {message} ===\n")

def capture_image(filename='photo.jpg'):
    cap = cv2.VideoCapture(0)  # Adjust the index if necessary
    ret, frame = cap.read()
    if ret:
        if not os.path.exists('pictures'):
            os.makedirs('pictures')
        cv2.imwrite(os.path.join('pictures', filename), frame)
    cap.release()
    return ret

def wait_for_start():
    pretty_print("Press START when ready.")
    while True:
        if ser.readline().decode('utf-8').strip() == "START":
            break
        sleep(0.1)

def select_option(options, option_type):
    pretty_print(f"Select a {option_type} by pressing the corresponding button:")
    for code, option in options.items():
        print(f"{code} - {option}")
    confirmed = False
    selected_option = None
    while not confirmed:
        ser.flushInput()  # Clear the serial buffer to avoid processing stale inputs
        line = ser.readline().decode('utf-8').strip()
        if line in options:
            selected_option = options[line]
            pretty_print(f"You selected {selected_option}. Press START to confirm or another button to change.")
        elif line == "START" and selected_option:
            confirmed = True
    return selected_option

def main():
    wait_for_start()

    pretty_print("Hello! This is a co-creation program with GPT. Let's get started! Press START.")
    wait_for_start()

    styles = {"GREEN": "Romeo and Juliet", "BLUE": "Sopranos", "YELLOW": "Star Trek"}
    settings = {"GREEN": "Mars", "BLUE": "Hairdresser", "YELLOW": "Classroom"}

    style = select_option(styles, "style")
    setting = select_option(settings, "setting")

    if capture_image():
        pretty_print("Image Captured Successfully!")
    else:
        pretty_print("Failed to capture image.")

    final_prompt = f"Please generate a two-minute improv theatre scene with the characters on the image. Setting: {setting}; Style: {style}."
    pretty_print(f"Resulted prompt would be: {final_prompt}")

if __name__ == "__main__":
    main()
