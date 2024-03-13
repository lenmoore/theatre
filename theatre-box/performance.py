from openai_interaction import get_improv_whisper
import pygame
import time
import os

dummy_scene = {
  "scene_name": "Phantom Flow",
  "dialogue": [
    {
      "name": "storyteller",
      "content": [
        "Welcome, folks, to the beat-bumpin', ghost-stompin' showdown in the haunted mansion. Where the living and the dead come to clash in a rap battle so fierce, it could wake the ancestors. Let's drop the beat and raise the spirits!",
        "On the left, we have the master of the mansion, the one, the only, Phantom Fred! And on the right, the challenger, a bold and daring visitor, MC Mortal! Let the rap battle begin!"
      ],
      "voice": "fable"
    },
    {
      "name": "Phantom Fred",
      "content": [
        "Yo, yo, yo, it's Phantom Fred on the mic,",
        "Haunting these halls every day and night.",
        "I've seen countless souls, but you, I dread,",
        "Because no one interrupts my undead thread."
      ],
      "voice": "echo"
    },
    {
      "name": "MC Mortal",
      "content": [
        "MC Mortal here, not afraid to fight,",
        "Battling ghosts in the dead of night.",
        "I might be living, but I’m ready to shred,",
        "Your rhymes are as dusty as this old homestead."
      ],
      "voice": "onyx"
    },
    {
      "name": "Phantom Fred",
      "content": [
        "I float, I haunt, I scare with flair,",
        "My verses chill the air, so you best prepare.",
        "This mansion's mine, from ceiling to bed,",
        "You'll flee in terror, by my rhymes be led."
      ],
      "voice": "echo"
    },
    {
      "name": "MC Mortal",
      "content": [
        "You think you're scary, but I'm the real deal,",
        "I've got the flow to make even ghosts feel.",
        "Your haunting days are about to end,",
        "Because I've got the power of a living friend!"
      ],
      "voice": "onyx"
    },
    {
      "name": "storyteller",
      "content": [
        "And so the battle raged, beats dropped, and spirits lifted. Until at last, the mansion filled with laughter more than fear. Who won, you ask? Well, in a showdown this legendary, everyone's a winner. Thanks for joining the phantom flow, where even the afterlife can't resist a good beat."
      ],
      "voice": "fable"
    }
  ]
}


def perform_scene(scene):
    print(scene)
    print(scene["scene_name"])

    order_number = 1
    character_channel = pygame.mixer.Channel(2)  # Assign speech to channel 1

    for part in scene["dialogue"]:
        print("part")
        print(part)
        voice = part["voice"]
        name = part["name"]
        merged_text = "... ".join(part["content"])
        if get_improv_whisper(order_number, voice, merged_text, name):
            sound_file = f'speech/improv/{order_number}_{name}_speech.mp3'
            speech_sound = pygame.mixer.Sound(sound_file)
            character_channel.play(speech_sound)

                # Wait for the speech sound to finish before continuing
            while character_channel.get_busy():
                time.sleep(0.1)  # Sleep to avoid busy waiting
        order_number += 1




if __name__ == "__main__":
    perform_scene(scene)