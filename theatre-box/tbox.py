import serial

from time import sleep
from hardware import read_from_arduino, capture_image
from printers import pretty_print, prompt_print


# Initialize serial port - replace 'COM3' with your Arduino's port
ser = serial.Serial('/dev/tty.usbmodem21101', 9600, timeout=1)
style = "Unknown"
setting = "Unknown"
drama = 0
comedy = 0

def wait_for_start():
    pretty_print("Press the red button when ready.")
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == "START":
            return True  # Start button pressed, exit the loop
        sleep(0.01)  # Check for start signal every 10ms


def main():
    global style, setting, drama, comedy

    pretty_print("--")
    pretty_print("Hello! I am the Director. Let's get started!")
    if wait_for_start():  # Wait for the first START to begin the process.

        pretty_print("--")
        pretty_print("I will guide you through the process of creating a theatre scene.")
        if wait_for_start():  # Wait for the second START.

            pretty_print("--")
            pretty_print("Please add a character on each of the platforms. You can also give them props.")
            if wait_for_start():  # Wait for the third START.

                pretty_print("--")
                pretty_print("You can tune some settings for the scene. Together we will build a prompt.")
                if wait_for_start():  # Wait for the fourth START, then proceed to read settings.

                    # Now, wait until settings are adjusted and final START is received.
                    while not read_from_arduino():
                        sleep(0.1)  # Adjust based on your needs, continue checking for updates from Arduino.

                    # Assuming read_from_arduino() will exit once final START is received after settings are done.
                    if capture_image():
                        pretty_print("Image Captured Successfully!")
                    else:
                        pretty_print("Failed to capture image.")



if __name__ == "__main__":
    main()
