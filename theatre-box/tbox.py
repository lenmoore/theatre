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
from image_controller import set_image_as_bg, open_image_in_thread
from colorama import Fore, Back, Style, init
from shared_event import close_window_signal

load_dotenv()

SERIAL_PORT1 = os.getenv("SERIAL_PORT1")
SERIAL_PORT2 = os.getenv("SERIAL_PORT2")


# Initialize serial port - replace 'COM3' with your Arduino's port
# UNCOMMENT TO ENABLE ARDUINO INTERACTION
ser = serial.Serial(SERIAL_PORT1, 9600, timeout=1)

style = "Undefined"
setting = "Undefined"
drama = 100
comedy = 50

scenes = {
    "Psychedelic Dreamscape": "pictures/A_psychedelic_dreamscape_5.png",
    "Carnival": "backgrounds/Carnival_1.png",
    "Dream": "backgrounds/dream.png",
    "Haunted house": "backgrounds/Haunted Mansion 5.png",
    "City street": "backgrounds/City Street 1.png",
    "Diner": "backgrounds/Diner .png",
    "Enchanted mushroom forest": "backgrounds/Ench.png",
    "Enchanted forest": "backgrounds/Enchanted.png",
    "Fairytale castle": "backgrounds/Fairytale Castle.png",
    "Hairdressers": "backgrounds/Hairdressers.png",
    "Pirate Ship": "backgrounds/pirateship1.png",
    "Pirate Ship On A Cliff": "backgrounds/Pirateship_6.png",
    "Mars after a spaceship crash": "backgrounds/Mars New 2.png",
    "Mars": "backgrounds/Mars.png",
    "Dreamworld": "backgrounds/Psychedelic Dreamscape.png",
    "Kopli tram": "backgrounds/Kopli tram 1.png",
    "Restaurant": "backgrounds/Restaurant 3.png",
    "Steampunk Airship": "backgrounds/Steampunk Airship 1.png",
    "Airship bridge": "backgrounds/Steampunk Airship 2.png",
    "Grand Budapest Hotel Lobby": "backgrounds/Wes Anderson 2.png"
}

scene_tracks = {
    "Psychedelic Dreamscape": "music/Dreamworld.mp3",
    "Carnival": "music/Carnival.mp3",
    "Dream": "music/Dream.mp3",
    "Haunted house": "music/Kummitusmaja.mp3",
    "City street": "music/Street.mp3",
    "Diner": "music/Diner.mp3",
    "Enchanted mushroom forest": "music/Enchanted forest.mp3",
    "Enchanted forest": "music/Enchanted forest.mp3",
    "Fairytale castle": "music/Fairytale castle.mp3",
    "Hairdressers": "music/Hairdressers.mp3",
    "Pirate Ship": "music/Piraadilaev.mp3",
    "Pirate Ship On A Cliff": "music/Piraadilaev.mp3",
    "Mars after a spaceship crash": "music/Mars Spaceship crash.mp3",
    "Mars": "music/Mars.mp3",
    "Dreamworld": "music/Dreamworld.mp3",
    "Kopli tram": "music/Tramm Koplis.mp3",
    "Restaurant": "music/Restaurant.mp3",
    "Steampunk Airship": "music/Steampunk airship.mp3",
    "Steampunk Airship bridge": "music/Steampunk airship.mp3",
    "Grand Budapest Hotel Lobby": "music/Grand Budapest Hotel Lobby.mp3"
}


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


def create_prompt_old():
#     director_says(1, "You are in testing mode. Uncomment directors lines.")
    director_says(1, "Hello, Director! Let's work on a scene for your upcoming play.")
    director_says(2, "As your assistant, I will guide you through the process of directing a theatre scene.")

    set_image_as_bg("BG2")
    director_says(3, "Pick characters from in front of the stage and place them on the platforms.")
    director_says(4, "These will be the characters of our scene.")
    director_says(5, "Press the red button to continue.")
    if wait_for_start():
#         director_says(5, "Use console now.")
        director_says(6, "Use the two rows of buttons to select a style and a setting for the scene.")
        director_says(7, "When you're ready, press the red button.")

        set_image_as_bg("BG1")
        while not read_from_arduino():
            sleep(0.01)  # Adjust based on your needs, continue checking for updates from Arduino.

        # Assuming read_from_arduino() will exit once final START is received after settings are done.
        if capture_image():
            pretty_print("Image captured successfully! Generating, please wait...")
            # Encode the image

            base64_image = encode_image()
            print("image encoded")
            return base64_image
        else:
            pretty_print("Failed to capture image.")

def choose_random_scenes(scenes, num_scenes=3):
    selected_scenes = random.sample(list(scenes.keys()), num_scenes)
    return selected_scenes  # Returns a list of three random scene names

def choose_style_and_setting():
    global style, setting
    director_says(6, "Use the two rows of buttons to select a style and a setting for the scene.")
    director_says(7, "When you're ready, press the red button to continue.")

    while True:
        if ser.inWaiting() > 0:
            line = ser.readline().decode('ascii', errors='replace').strip()
            print_current_prompt(setting, style, drama, comedy)

            print_section("STYLES", styles, style, Back.RED)
            print_section("SETTINGS", settings, setting, Back.GREEN)

            if line.startswith("STYLE"):
                index = int(line.replace("STYLE", ""))
                style = styles[index]
            elif line.startswith("SCENE"):
                index = int(line.replace("SCENE", ""))
                setting = settings[index]
            elif line == "START":
                if style.startswith("Undef"):
                    director_says(31, "Please select a style using the small red buttons.")
                elif setting.startswith("Undef"):
                    director_says(32, "Please select a location setting using the small white buttons.")
                else:
                    director_says(33, "Now use the dials to set the values for drama and comedy.")
                    return True

#     print_current_prompt(setting, style, drama, comedy)
def choose_drama_and_comedy():
    global drama, comedy
    global style, setting


    while True:
        if ser.inWaiting() > 0:
            line = ser.readline().decode('ascii', errors='replace').strip()
            print_current_prompt(setting, style, drama, comedy, 60, True)
            if line.startswith("COMEDY"):
                value_str = line.replace("COMEDY", "").strip()
                if value_str.isdigit():
                    comedy = int(value_str)
            elif line.startswith("DRAMA"):
                value_str = line.replace("DRAMA", "").strip()
                if value_str.isdigit():
                    drama = int(value_str)
            elif line == "START":
                if drama == 100 and comedy == 50:
                    director_says(35, "Please adjust the dials to set the values for drama and comedy.")
                else:
                    return True

def create_prompt():
    director_says(1, "Hello, Director!")
    director_says(2, "I will guide you through the process of directing a theatre scene for your upcoming play.")
    director_says(3, "Pick characters from in front of the stage and place them on the platforms.")
    set_image_as_bg("BG2")
    director_says(4, "These will be the characters of our scene. I know you'll make the right choice.")
    director_says(5, "Press the red button to continue.")
    if wait_for_start():
        if choose_style_and_setting():
            if choose_drama_and_comedy():
                set_image_as_bg("Black")
                base64_image = capture_image()
                if base64_image:
                    director_says(6, "Great! Now I will generate a theatre scene based on your direction:")
                    # Continue with scene generation
                    return base64_image
                else:
                    pretty_print("Failed to capture image.")


def read_from_arduino():
    global style, setting, drama, comedy
    global styles, settings
    while True:
        try:
            # Print style and setting options with one selected
            print("")
            print("")
            print("")
            print("")
            print_current_prompt(setting, style, drama, comedy)
            print_section("STYLES", styles, style, Back.RED)
            print_section("SETTINGS", settings, setting, Back.GREEN)
            if ser.inWaiting() > 0:  # Check if data is available
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line == "START":
                    print("ENTER")
                    if (style.startswith("Undef")):
                        director_says(31, "Please select a style using the small red buttons.")
                    elif (setting.startswith("Undef")):
                        director_says(32, "Please select a location setting using the small white buttons.")
                    else:
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
                    print("En signal received")
                    start_received = True
                    return True
                last_start_time = time.time()
        else:
            time.sleep(0.1)

def main():
    global style, setting, drama, comedy, background_channel, speech_channel
    global styles, settings

    set_image_as_bg("BG1")
    random_scenes = choose_random_scenes(scenes)
    option1, option2, option3 = random_scenes
    settings = [option1, option2, option3]

    random_styles = choose_random_scenes({"Rap Battle":"", "Fairy Tale":"", "Shakespeare":"",  "Neuromancer":"", "Medieval bard duet":"", "Dr Seuss":"", "Edgar Allan Poe": "" })
    style1, style2, style3 = random_styles
    styles = style1, style2, style3

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
        background_music = pygame.mixer.Sound("music/loading.mp3")
        background_music.set_volume(0.5)
        background_channel.play(background_music, loops=-1)

        print_current_prompt(setting, style, drama, comedy, 100, True)
        background_music.set_volume(0.05)

        director_says(9, "Some patience, please!")
        background_music.set_volume(0.5)
        image_path = "../pictures/photo.jpg"
#         open_image_in_thread("pictures/photo.jpg")
#         open_user_photo()
        prompt = f"2 minute improv scene, setting: {setting}, style: {style}, drama: {drama}/100, comedy: {comedy}/100"
        pretty_print("Painting the stage... The scene: " + setting)
        set_image_as_bg(setting)
        pretty_print("Generating characters...")

        result = create_openai_request(base64_image, prompt)
        background_music.set_volume(0.05)

        director_says(10, "Almost there!")
        pretty_print("Writing the scene...")
        background_music.set_volume(0.5)

        scene = create_openai_scene(result, prompt)
        pretty_print("Scene created!")
        background_channel.stop()
        time.sleep(0.1)
        director_says(9, "Oh.... I'm so excited!  ")

#         os.system('xdotool search --name "Konsole" | xargs xdotool windowactivate')

        # todo: play correct background music
#         selected_scene_music = pygame.mixer.Sound(f"music/{scene['scene_name']}.mp3")
#         background_channel.play(selected_scene_music, loops=-1)
        sceneready_music = pygame.mixer.Sound("music/scene-ready.mp3")

        background_music.set_volume(0.1)
        background_channel.play(sceneready_music)
        sleep(2)

        if scene_tracks.get(setting):
            background_music.set_volume(0.05)
            scene_music = pygame.mixer.Sound(scene_tracks.get(setting))
            background_channel.play(scene_music)
        perform_scene(scene)

    # Stop the background music after all speech has been played
    background_channel.stop()
    # todo: remove the files from the director and improv folders
    director_says(8, "..... and SCENE! BRAVO! Even better than the last one. Wow, such genius! I think you should write another one, Director.")
    close_window_signal.set()
    # empty the director and improv folders
    set_image_as_bg("BG1")

    clear_folders()
     # Inform user to press start to play again
    director_says(9, "OK, press the red button to play again")

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
