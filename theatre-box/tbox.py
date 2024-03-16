import serial
import pygame
import time
import os
from time import sleep
from hardware import capture_image
from printers import pretty_print, prompt_print, prompt_print_no_start
from openai_interaction import get_whisper, create_openai_request, create_openai_scene
from performance import perform_scene
import requests
from playsound import playsound
from dotenv import load_dotenv
import json

load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT")


# Initialize serial port - replace 'COM3' with your Arduino's port
# UNCOMMENT TO ENABLE ARDUINO INTERACTION
ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)

# style = "storyteller werner herzog documentary"
style = "Undefined"
setting = "Undefined"
drama = 100
comedy = 50

# SETTINGS
# 6am at berghain
# 90s kopli tram
# ER waiting room 8:30am
# festival outdoor toilet queue before main performer
# football arena parking lot moments before the local team loses

# STYLES
# neuromancer
# werner herzog documentary
# rap battle
# romeo and juliet
# fairy tale [and when it is chosen, select one from any of Grimm or HC Andersen's repertoire ]
def read_from_arduino():
    global style, setting, drama, comedy
    while True:
        try:
            if ser.inWaiting() > 0:  # Check if data is available
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line.startswith("STYLE"):
                    index = int(line.replace("STYLE", ""))
                    styles = ["Romeo and Juliet", "Rap battle", "West Side Story"]
                    style = styles[index]
                    prompt_print(setting, style, drama, comedy)
                elif line.startswith("SCENE"):
                    index = int(line.replace("SCENE", ""))
                    settings = ["Mars", "Haunted mansion", "90s Kopli tram"]
                    setting = settings[index]
                    prompt_print(setting, style, drama, comedy)
                elif line.startswith("DRAMA"):
                    drama = int(float(line.replace("DRAMA", "")))
                    prompt_print(setting, style, drama, comedy)
                elif line.startswith("COMEDY"):
                    comedy = int(float(line.replace("COMEDY", "")))
                    prompt_print(setting, style, drama, comedy)
                elif line == "START":
                    print("START signal received")
                    return True  # Start button pressed, exit the function
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
        time.sleep(0.01)  # Small delay to avoid overwhelming the CPU


start_received = False
start_cooldown = 2  # Cooldown period in seconds

def wait_for_start():
    global start_received
    pretty_print("Press the red button when ready.")
    last_start_time = 0
    while True:
        if ser.inWaiting() > 0:
            line = ser.readline().decode('ascii', errors='replace').strip()
            if line == "START" and (time.time() - last_start_time > start_cooldown):
                if not start_received:
                    print("START signal received")
                    start_received = True
                    return True
                last_start_time = time.time()
        else:
            time.sleep(0.01)

# # UNCOMMENT FOR ARDUINO
# def wait_for_start():
#     pretty_print("Waiting for big red button press...")
#     while True:
#         try:
#             if ser.inWaiting() > 0:  # Check if data is available
#                 line = ser.readline().decode('ascii', errors='replace').strip()
#                 if line == "START":
#                     print("START signal received")
#                     return True  # Start button pressed, exit the loop
#         except Exception as e:
#             print(f"Error waiting for start signal: {e}")
#         time.sleep(0.01)  # Check for start signal every 10ms, adjust as necessary for responsiveness vs CPU usage

def print_and_talk(text, voice):
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("")
    pretty_print("--")
    # print empty line
    pretty_print(text)
    get_whisper(1, "nova", text)
    speech_channel.play(speech_sound)

    # Wait for the speech sound to finish before continuing
    while speech_channel.get_busy():
        time.sleep(0.1)  # Sleep to avoid busy waiting

def director_says(order_number, text):
    pretty_print("--")
    pretty_print(text)
    if get_whisper(order_number, "shimmer", text):
        sound_file = f'speech/director/{order_number}_director_speech.mp3'
        speech_sound = pygame.mixer.Sound(sound_file)
        speech_channel.play(speech_sound)

        # Wait for the speech sound to finish before continuing
    while speech_channel.get_busy():
        time.sleep(0.1)  # Sleep to avoid busy waiting


def create_prompt():
    director_says(1, "Hello! I am the Director. Let's get started!")
    director_says(2, "I will guide you through the process of creating a theatre scene.")
    director_says(3, "Please add a character on each of the platforms. You can also give them props.")
    director_says(4, "When you're ready, press the red button.")

    if wait_for_start():
        director_says(5, "You can tune some settings for the scene. Together we will build a prompt.")
        director_says(6, "Press the red button when ready.")

        while not read_from_arduino():
            sleep(0.01)  # Adjust based on your needs, continue checking for updates from Arduino.

        # Assuming read_from_arduino() will exit once final START is received after settings are done.
        if capture_image():
            pretty_print("Image captured successfully! Generating, please wait...")
            return True
        else:
            pretty_print("Failed to capture image.")

def main():
    global style, setting, drama, comedy, background_channel, speech_channel
    pygame.mixer.init() # Initialize the mixer module
    background_music = pygame.mixer.Sound("music/theme.mp3") # file
    background_channel = pygame.mixer.Channel(0)  # Assign background music to channel 0
    background_channel.play(background_music, loops=-1)  # -1 means the music will loop indefinitely
    background_music.set_volume(0.05)
    # Ensure the background music continues to play
    if not background_channel.get_busy():
        background_channel.play(background_music, loops=-1)


    speech_channel = pygame.mixer.Channel(1)  # Assign speech to channel 1
    if create_prompt():
        director_says(6, "Great! Now I will generate a theatre scene based on the final prompt:")
        background_music = pygame.mixer.Sound("music/loading.mp3")
        background_channel.play(background_music, loops=-1)

        director_says(9, "Some patience, please!")

        prompt_print_no_start(setting, style, drama, comedy)

        prompt = (f"""           The current prompt is:
                               Please generate a two-minute improv theatre scene
                             with the characters on the stage.
                           Setting: {setting}
                               Style: {style}
                              Drama: {drama}/100
                           Comedy: {comedy}/100

        """)
        image_path = "../pictures/Photo March 2 2024.jpg"
        result = create_openai_request(image_path, prompt)
        director_says(10, "Almost there!")
        scene = create_openai_scene(result, prompt)
        background_channel.stop()
        time.sleep(0.1)
        director_says(9, "Oh.... I'm so excited!")
        time.sleep(3)
        # open an image file
#         image_path = f"../backgrounds/{scene['scene_name']}.jpg"
        image_path = f"backgrounds/Carnival_1.png"
        img = pygame.image.load(image_path)
        time.sleep(3)

        # todo: play correct background music
#         selected_scene_music = pygame.mixer.Sound(f"music/{scene['scene_name']}.mp3")
#         background_channel.play(selected_scene_music, loops=-1)
        sceneready_music = pygame.mixer.Sound("music/scene-ready.mp3")
        background_channel.play(sceneready_music)

        perform_scene(scene)

    # Stop the background music after all speech has been played
    background_channel.stop()
    # todo: remove the files from the director and improv folders
    director_says(8, "Thank you. I hope you enjoyed the performance. Goodbye!")

    # empty the director and improv folders
    folder = "speech/director"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    folder = "speech/improv"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)



if __name__ == "__main__":
    main()
