import serial
import pygame
import time
import os
from time import sleep
from hardware import capture_image, encode_image
from printers import pretty_print, print_current_prompt, print_section
from openai_interaction import get_whisper, create_openai_request, create_openai_scene
from performance import perform_scene
import requests
from playsound import playsound
from dotenv import load_dotenv
import json
import random
from image_controller import open_image_in_thread
from colorama import Fore, Back, Style, init
from shared_event import close_window_signal

load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT")


# Initialize serial port - replace 'COM3' with your Arduino's port
# UNCOMMENT TO ENABLE ARDUINO INTERACTION
ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)

style = "Undefined"
setting = "Undefined"
drama = 100
comedy = 50

scenes = {
    "Carnival": "backgrounds/Carnival_1.png",
    "Dream": "backgrounds/Carol Style .png",
    "City street": "backgrounds/City Street 1.png",
    "Diner": "backgrounds/Diner .png",
    "Enchanted mushroom forest": "backgrounds/Ench.png",
    "Enchanted forest": "backgrounds/Enchanted.png",
    "Fairytale castle": "backgrounds/Fairytale Castle.png",
    "Hairdressers": "backgrounds/Hairdressers.png",
    "Pirate Ship": "backgrounds/pirateship1.png",
    "Mars after a spaceship crash": "backgrounds/Mars New 2.png",
    "Mars": "backgrounds/Mars.png",
    "Dreamworld": "backgrounds/Psychedelic Dreamscape.png",
    "Kopli tram": "backgrounds/Kopli tram 1.png",
    "Restaurant": "backgrounds/Restaurant 3.png",
    "Steampunk Airship": "backgrounds/Steampunk Airship 1.png",
    "Airship bridge": "backgrounds/Steampunk Airship 2.png",
    "Grand Budapest Hotel Lobby": "backgrounds/Wes Anderson 2.png"
}

def read_from_arduino():
    global style, setting, drama, comedy
    while True:
        try:
            # Print style and setting options with one selected
            print("")
            print("")
            print_section("STYLES", styles, style, Back.RED)
            print_section("SETTINGS", settings, setting, Back.GREEN)
            if ser.inWaiting() > 0:  # Check if data is available
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line == "START":
                    print("START signal received")
                    return True  # Start button pressed, exit the function
                elif line.startswith("STYLE"):
                    index = int(line.replace("STYLE", ""))
                    style = styles[index]
#                     print_current_prompt(setting, style, drama, comedy)
                elif line.startswith("SCENE"):
                    index = int(line.replace("SCENE", ""))
                    setting = settings[index]
#                     print_current_prompt(setting, style, drama, comedy)
                elif line.startswith("DRAMA"):
                    drama = int(float(line.replace("DRAMA", "")))
#                     print_current_prompt(setting, style, drama, comedy)
                elif line.startswith("COMEDY"):
                    comedy = int(float(line.replace("COMEDY", "")))
#                     print_current_prompt(setting, style, drama, comedy)
                print_current_prompt(setting, style, drama, comedy)

        except Exception as e:
            print(f"Error reading from Arduino: {e}")
        time.sleep(0.01)  # Small delay to avoid overwhelming the CPU


start_cooldown = 0.05  # Cooldown period in seconds

def wait_for_start():
    global start_received
    start_received = False
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
            time.sleep(0.1)

def clear_folders():
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
    director_says(1, "You are in testing mode. Uncomment directors lines.")
#     director_says(1, "Hello! I am the Director. Let's get started!")
#     director_says(2, "I will guide you through the process of creating a theatre scene.")
#     director_says(3, "Please add a character on each of the platforms. You can also give them props.")
#     director_says(4, "When you're ready, press the red button.")

    if wait_for_start():
        director_says(5, "Use console now.")
#         director_says(5, "You can tune some settings for the scene. Together we will build a prompt.")
#         director_says(6, "Use the console to set up your prompt. When you're ready, press the red button.")

        while not read_from_arduino():
            sleep(0.01)  # Adjust based on your needs, continue checking for updates from Arduino.

        # Assuming read_from_arduino() will exit once final START is received after settings are done.
        if capture_image():
            pretty_print("Image captured successfully! Generating, please wait...")
            # Encode the image
            base64_image = encode_image()
            return base64_image
        else:
            pretty_print("Failed to capture image.")

def choose_random_scenes(scenes, num_scenes=3):
    selected_scenes = random.sample(list(scenes.keys()), num_scenes)
    return selected_scenes  # Returns a list of three random scene names

# todo
# def introduce_character(position):
#     director_says(12, f"Introducing the character on the {position} platform.")
#     director_says(13, f"Introducing the character on the {position} platform.")

def main():
    global style, setting, drama, comedy, background_channel, speech_channel
    global styles, settings

    random_scenes = choose_random_scenes(scenes)
    option1, option2, option3 = random_scenes

    settings = [option1, option2, option3]
    styles = ["Rap Battle", "Fairy Tale", "Shakespeare"]

    pygame.init()  # Initialize the pygame module
    pygame.mixer.init() # Initialize the mixer module
    background_music = pygame.mixer.Sound("music/theme.mp3") # file
    background_channel = pygame.mixer.Channel(0)  # Assign background music to channel 0
    background_channel.play(background_music, loops=-1)  # -1 means the music will loop indefinitely
    background_music.set_volume(0.05)
    # Ensure the background music continues to play
    if not background_channel.get_busy():
        background_channel.play(background_music, loops=-1)


    speech_channel = pygame.mixer.Channel(1)  # Assign speech to channel 1
    base64_image = create_prompt()
    if base64_image:
        director_says(6, "Great! Now I will generate a theatre scene based on the final prompt:")
        background_music = pygame.mixer.Sound("music/loading.mp3")
        background_channel.play(background_music, loops=-1)

        print_current_prompt(setting, style, drama, comedy)
        director_says(9, "Some patience, please!")
        image_path = "../pictures/photo.jpg"
        prompt = f"2 minute improv scene, setting: {setting}, style: {style}, drama: {drama}/100, comedy: {comedy}/100"
        pretty_print("Painting the stage...")
        print(setting)
        open_image_in_thread(setting)
        pretty_print("Generating characters...")
        result = create_openai_request(base64_image, prompt)
        director_says(10, "Almost there!")
        pretty_print("Writing the scene...")
        scene = create_openai_scene(result, prompt)
        pretty_print("Scene created!")
        background_channel.stop()
        time.sleep(0.1)
        director_says(9, "Oh.... I'm so excited! ")
#         introduce_character("left")
#         introduce_character("right")
        os.system('xdotool search --name "Konsole" | xargs xdotool windowactivate')

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
    close_window_signal.set()
    # empty the director and improv folders

    clear_folders()
     # Inform user to press start to play again
    director_says(9, "OK, press start to play again")

    # Reset global variables if necessary
    style = "Undefined"
    setting = "Undefined"
    drama = 100
    comedy = 50
    start_received = False  # Reset the start received flag

    # Wait for the user to press start to restart the game
    if wait_for_start():
        # Once start is received, call main() again to restart the game
        main()




if __name__ == "__main__":
    main()
