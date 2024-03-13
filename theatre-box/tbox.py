import serial
import pygame
import time
import os
from time import sleep
from hardware import capture_image
from printers import pretty_print, prompt_print
from openai_interaction import get_whisper, create_openai_request, create_openai_scene
from performance import perform_scene
import requests
from playsound import playsound

import json

# Initialize serial port - replace 'COM3' with your Arduino's port
# UNCOMMENT TO ENABLE ARDUINO INTERACTION
# ser = serial.Serial('/dev/tty.usbmodem21101', 9600, timeout=1)

# style = "storyteller werner herzog documentary"
style = "Fish-out-of-Water"
setting = "Haunted mansion"
drama = 100
comedy = 100

def read_from_arduino():
    global style, setting, drama, comedy
    while ser.inWaiting() > 0:  # Check if data is available
        line = ser.readline().decode('utf-8').strip()
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
            drama = int(line.replace("DRAMA", ""))
            prompt_print(setting, style, drama, comedy)
        elif line.startswith("COMEDY"):
            comedy = int(line.replace("COMEDY", ""))
            prompt_print(setting, style, drama, comedy)
        elif line == "START":
            return True  # Start button pressed
    return False  # Start button not pressed

def wait_for_start():
    return True
#     pretty_print("Press the red button when ready.")
#     while True:
#         line = ser.readline().decode('utf-8').strip()
#         if line == "START":
#             return True  # Start button pressed, exit the loop
#         sleep(0.01)  # Check for start signal every 10ms

def print_and_talk(text, voice):
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
    if get_whisper(order_number, "nova", text):
        sound_file = f'speech/director/{order_number}_director_speech.mp3'
        speech_sound = pygame.mixer.Sound(sound_file)
        speech_channel.play(speech_sound)

        # Wait for the speech sound to finish before continuing
    while speech_channel.get_busy():
        time.sleep(0.1)  # Sleep to avoid busy waiting


def create_prompt():
    director_says(1, "Hello! I am the Director. Let's get started!")

    if wait_for_start():
        director_says(2, "I will guide you through the process of creating a theatre scene.")

        if wait_for_start():
            director_says(3, "Please add a character on each of the platforms. You can also give them props.")

            if wait_for_start():
                director_says(4, "You can tune some settings for the scene. Together we will build a prompt.")

                if wait_for_start():
                    # Now, wait until settings are adjusted and final START is received.
                    director_says(5, "Tune the settings for the scene and press the red button when ready.")

#                     UNCOMMENT TO ENABLE ARDUINO INTERACTION
#                     while not read_from_arduino():
#                         sleep(0.01)  # Adjust based on your needs, continue checking for updates from Arduino.

                    # Assuming read_from_arduino() will exit once final START is received after settings are done.
                    if capture_image():
                        pretty_print("Image Captured Successfully!")
                        return True
                    else:
                        pretty_print("Failed to capture image.")

def main():
    global style, setting, drama, comedy, background_channel, speech_channel
    pygame.mixer.init() # Initialize the mixer module
    background_music = pygame.mixer.Sound("music/TBox Theme Song.mp3") # file
    background_channel = pygame.mixer.Channel(0)  # Assign background music to channel 0
    background_channel.play(background_music, loops=-1)  # -1 means the music will loop indefinitely
    background_music.set_volume(0.05)  # Set to 50% volume; adjust as needed
    # Ensure the background music continues to play
    if not background_channel.get_busy():
        background_channel.play(background_music, loops=-1)


    speech_channel = pygame.mixer.Channel(1)  # Assign speech to channel 1
    if create_prompt():
        director_says(6, "Great! Now I will generate a theatre scene based on the final prompt:")

        # todo: play waiting music
        prompt_print(setting, style, drama, comedy)

        prompt = (f"""           The current prompt is:
                               Please generate a two-minute improv theatre scene
                             with the characters on the stage.
                           Setting: {setting}
                               Style: {style}
                              Drama: {drama}/100
                           Comedy: {comedy}/100
                   When you are totally sure that you're ready with the prompt,'
                          press START.

        """)
        image_path = "../pictures/Photo March 2 2024.jpg"
        result = create_openai_request(image_path)
        scene = create_openai_scene(result, prompt)
        # todo: play correct background music
#         selected_scene_music = pygame.mixer.Sound(f"music/{scene['scene_name']}.mp3")
#         background_channel.play(selected_scene_music, loops=-1)
        background_channel.stop()

        perform_scene(scene)

    # Stop the background music after all speech has been played
    background_channel.stop()
    # todo: remove the files from the director and improv folders
    director_says(8, "Thank you. I hope you enjoyed the performance. Goodbye!")



if __name__ == "__main__":
    main()
