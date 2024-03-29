from openai_interaction import get_improv_whisper
import pygame
import time
import os
from printers import print_dialogue
from image_controller import open_image_in_thread

def perform_scene(scene):
    print(scene["scene_name"])

    order_number = 1
    character_channel = pygame.mixer.Channel(2)  # Assign speech to channel 1

    for part in scene["dialogue"]:
        voice = part["voice"]
        name = part["name"]
        merged_text = "... ".join(part["content"])
        if get_improv_whisper(order_number, voice, merged_text, name):
            sound_file = f'speech/improv/{order_number}_{name}_speech.mp3'
            speech_sound = pygame.mixer.Sound(sound_file)
            print(name)
            print_dialogue(part, voice)
            character_channel.play(speech_sound)

                # Wait for the speech sound to finish before continuing
            while character_channel.get_busy():
                time.sleep(0.1)  # Sleep to avoid busy waiting
        order_number += 1




if __name__ == "__main__":
    perform_scene(scene)