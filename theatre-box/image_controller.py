import pygame
import os
from tkinter import Tk, Canvas, PhotoImage
os.environ['SDL_VIDEODRIVER'] = 'x11'
os.environ['SDL_VIDEO_CENTERED'] = '1'

image_paths = {
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

def open_image(image_name):
    root = Tk()
    canvas = Canvas(root, width=1200, height=900)
    canvas.pack()
    image = image_paths.get(image_name)
    img = PhotoImage(file=image)
    canvas.create_image(20, 20, anchor='nw', image=img)
    root.mainloop()
# def open_image(scene_name):
#     pygame.init()
#     screen = pygame.display.set_mode((1200, 900))
#
#
#
#     image = image_paths.get(scene_name, "backgrounds/Carnival_1.png")  # Default to Carnival if not found
#     background = pygame.image.load(image).convert()
# #     screen.blit(background, (background, 0))
# #     pygame.display.flip()
#
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#     pygame.quit()

if __name__ == "__main__":
    open_image("Carnival")
